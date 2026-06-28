#!/usr/bin/env python
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib import request


UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36"


def refresh_windows_path():
    if os.name != "nt":
        return
    parts = [
        os.environ.get("PATH", ""),
        os.environ.get("Path", ""),
    ]
    for scope in ("Machine", "User"):
        try:
            value = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    f"[Environment]::GetEnvironmentVariable('Path','{scope}')",
                ],
                text=True,
                encoding="utf-8",
                errors="replace",
                capture_output=True,
                timeout=10,
            )
            if value.returncode == 0:
                parts.append(value.stdout.strip())
        except Exception:
            pass
    os.environ["PATH"] = ";".join(part for part in parts if part)


def fail(message, code=1):
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(code)


def run(cmd):
    result = subprocess.run(cmd, text=True, encoding="utf-8", errors="replace", capture_output=True)
    if result.returncode != 0:
        if result.stdout:
            print(result.stdout, file=sys.stderr)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        fail(f"command failed: {' '.join(map(str, cmd))}")
    return result.stdout


def http_json(url, referer="https://www.bilibili.com/"):
    req = request.Request(url, headers={"User-Agent": UA, "Referer": referer})
    with request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def download(url, dest, referer):
    req = request.Request(url, headers={"User-Agent": UA, "Referer": referer})
    with request.urlopen(req, timeout=120) as resp, open(dest, "wb") as fh:
        shutil.copyfileobj(resp, fh)
    return dest


def safe_slug(value):
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip())
    return value.strip("-")[:80] or "video"


def output_root(source, output_dir):
    if output_dir:
        root = Path(output_dir)
    else:
        stem = safe_slug(Path(source).stem if Path(source).exists() else source)
        root = Path(tempfile.gettempdir()) / f"video-transcribe-{stem}"
    root.mkdir(parents=True, exist_ok=True)
    return root


def get_bilibili_audio(source, root):
    match = re.search(r"(BV[0-9A-Za-z]+)", source)
    if not match:
        return None
    bvid = match.group(1)
    view = http_json(f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}")
    if view.get("code") != 0:
        fail(f"Bilibili view API failed: {view.get('message')}")
    data = view["data"]
    cid = data["cid"]
    referer = f"https://www.bilibili.com/video/{bvid}/"
    play = http_json(
        f"https://api.bilibili.com/x/player/playurl?bvid={bvid}&cid={cid}&fnval=16&fourk=1",
        referer=referer,
    )
    audio_streams = (((play.get("data") or {}).get("dash") or {}).get("audio") or [])
    if not audio_streams:
        fail("Bilibili playurl API returned no DASH audio stream")
    best = max(audio_streams, key=lambda item: item.get("bandwidth", 0))
    raw = root / "audio.m4s"
    download(best.get("baseUrl") or best.get("base_url"), raw, referer)
    return {
        "platform": "bilibili",
        "id": bvid,
        "title": data.get("title") or bvid,
        "raw_audio": str(raw),
    }


def get_ytdlp_audio(source, root):
    if not re.match(r"https?://", source):
        return None
    if not shutil.which("yt-dlp"):
        fail("yt-dlp is required for non-Bilibili URLs but was not found")
    before = {p.resolve() for p in root.glob("*")}
    template = str(root / "source.%(ext)s")
    run(["yt-dlp", "--no-playlist", "-f", "bestaudio/best", "-o", template, source])
    after = [p for p in root.glob("source.*") if p.resolve() not in before]
    if not after:
        after = list(root.glob("source.*"))
    if not after:
        fail("yt-dlp completed but no source audio/video file was found")
    return {
        "platform": "yt-dlp",
        "id": source,
        "title": source,
        "raw_audio": str(max(after, key=lambda p: p.stat().st_mtime)),
    }


def convert_to_wav(input_path, wav_path):
    if not shutil.which("ffmpeg"):
        fail("ffmpeg not found. Install Gyan.FFmpeg or add ffmpeg to PATH.")
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(input_path), "-ar", "16000", "-ac", "1", str(wav_path)])


def transcribe(wav_path, transcript_path, model_name, language):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        fail("faster-whisper is not installed in this Python. Install with: python -m pip install faster-whisper socksio")

    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    lang = None if language == "auto" else language
    segments, info = model.transcribe(str(wav_path), language=lang, vad_filter=False, beam_size=5)
    lines = []
    for segment in segments:
        text = segment.text.strip()
        if text:
            lines.append(f"[{segment.start:06.2f}-{segment.end:06.2f}] {text}")
    transcript_path.write_text("\n".join(lines), encoding="utf-8")
    return {"language": info.language, "language_probability": info.language_probability, "segments": len(lines)}


def main():
    refresh_windows_path()
    parser = argparse.ArgumentParser(description="Extract audio from a video URL/file and transcribe it with local faster-whisper.")
    parser.add_argument("source", help="Bilibili URL/BV id, YouTube/generic URL, or local audio/video file")
    parser.add_argument("--output-dir", help="Directory for audio.wav, transcript.txt, and metadata.json")
    parser.add_argument("--model", default="base", help="faster-whisper model name or local model path")
    parser.add_argument("--language", default="auto", help="Language code such as zh/en, or auto")
    args = parser.parse_args()

    source = args.source
    root = output_root(source, args.output_dir)
    wav = root / "audio.wav"
    transcript_path = root / "transcript.txt"
    metadata_path = root / "metadata.json"

    local = Path(source)
    if local.exists():
        meta = {"platform": "local", "id": str(local), "title": local.name, "raw_audio": str(local)}
    else:
        meta = get_bilibili_audio(source, root) or get_ytdlp_audio(source, root)

    convert_to_wav(meta["raw_audio"], wav)
    transcript_meta = transcribe(wav, transcript_path, args.model, args.language)
    meta.update(transcript_meta)
    meta.update({
        "source": source,
        "wav_path": str(wav),
        "transcript_path": str(transcript_path),
        "metadata_path": str(metadata_path),
        "model": args.model,
        "requested_language": args.language,
    })
    metadata_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"platform={meta['platform']}")
    print(f"title={meta.get('title', '')}")
    print(f"wav_path={wav}")
    print(f"transcript_path={transcript_path}")
    print(f"metadata_path={metadata_path}")
    print(f"segments={meta['segments']} language={meta['language']} probability={meta['language_probability']:.3f}")


if __name__ == "__main__":
    main()
