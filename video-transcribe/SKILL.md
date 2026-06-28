---
name: video-transcribe
description: Transcribe and summarize video links or local audio/video files when the user shares a Bilibili, YouTube, or other video URL and asks Codex to watch, read, summarize, extract key points, or turn the content into notes. Use this for videos without available subtitles by extracting audio, converting it with ffmpeg, and running local faster-whisper.
---

# Video Transcribe

## Overview

Use this skill when a user gives a video link and wants Codex to understand the spoken content. Prefer existing subtitles when a platform exposes them; when subtitles are missing, use `scripts/transcribe_video.py` to extract audio and create a timestamped transcript.

The model should make judgment calls only after transcript text exists: summarize, classify, extract action items, or answer questions from the transcript. Downloading, retrying, platform routing, transcoding, and file checks belong to the script or deterministic shell commands.

## Workflow

1. State assumptions and success criteria.
2. If the user provided only a URL, infer the target as "transcribe and summarize" unless they asked for another output.
3. Run the script:

```powershell
$skill = "C:\Users\qtr82\.codex\skills\video-transcribe"
$py = "C:\Users\qtr82\.agent-reach\local-whisper-venv\Scripts\python.exe"
& $py "$skill\scripts\transcribe_video.py" "VIDEO_URL_OR_LOCAL_FILE"
```

4. Read the printed `transcript_path`.
5. Summarize from the transcript and explicitly mention any quality caveats.

For Chinese videos, use `--language zh` if auto-detection produces unstable text:

```powershell
& $py "$skill\scripts\transcribe_video.py" "VIDEO_URL_OR_LOCAL_FILE" --language zh --model base
```

## Environment

Expected local setup on this machine:

- `ffmpeg` from `Gyan.FFmpeg`, available through WinGet links.
- local Whisper venv at `C:\Users\qtr82\.agent-reach\local-whisper-venv`.
- Python packages in that venv: `faster-whisper` and `socksio`.

If the venv is missing, recreate it without touching the project repo:

```powershell
$venv = "C:\Users\qtr82\.agent-reach\local-whisper-venv"
C:\Users\qtr82\.agent-reach-venv\Scripts\python.exe -m venv $venv
& "$venv\Scripts\python.exe" -m pip install --upgrade pip
& "$venv\Scripts\python.exe" -m pip install faster-whisper socksio
```

If `ffmpeg` is missing:

```powershell
winget install --id Gyan.FFmpeg --exact --accept-package-agreements --accept-source-agreements --silent
```

After installing `ffmpeg`, refresh the current PowerShell process path before retrying:

```powershell
$env:Path = [Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [Environment]::GetEnvironmentVariable("Path","User") + ";" + $env:Path
```

## Script Behavior

`scripts/transcribe_video.py` supports:

- Bilibili URLs or BV ids: uses Bilibili public view/playurl APIs and downloads the highest-bandwidth DASH audio stream. Do not use `yt-dlp` for Bilibili.
- YouTube and generic video URLs: uses `yt-dlp` when available.
- local audio/video paths: converts directly with `ffmpeg`.

Outputs are written under `%TEMP%\video-transcribe-...` unless `--output-dir` is provided:

- `audio.wav`: 16 kHz mono audio for Whisper.
- `transcript.txt`: timestamped transcript.
- `metadata.json`: source, title, platform, output paths, model, and language.

## Quality Rules

- Do not claim exact wording when using local Whisper unless the transcript is clean.
- Normalize obvious ASR errors in the final summary, especially product names and repeated terms. Common examples from Chinese ASR are Harness, Codex, AGENTS.md, Superpowers, and acceptance criteria.
- If the script fails because the platform blocks audio or a dependency is missing, report the exact blocker and the command that would verify the fix.
- Keep temporary artifacts in `%TEMP%`; do not create files in the user's project unless they ask for exported notes.
