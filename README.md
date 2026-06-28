# Video Transcribe Skill

> A local Codex skill for turning video links into timestamped transcripts and summaries.

English | [中文](#中文)

## Why

Many useful videos have no subtitles, especially short Bilibili demos and tutorials. This skill gives Codex a repeatable path to "watch" those videos by using deterministic tooling first:

1. resolve the video source,
2. extract the audio,
3. normalize it with FFmpeg,
4. transcribe it locally with faster-whisper,
5. let the model summarize or extract answers from the transcript.

No cloud transcription key is required.

## Features

- Bilibili URL and BV id support through public Bilibili APIs.
- YouTube and generic URL fallback through `yt-dlp`.
- Local audio/video file support.
- Local `faster-whisper` transcription on CPU.
- Timestamped `transcript.txt` output.
- `metadata.json` with source, platform, language, paths, and model.
- Codex skill metadata through `SKILL.md` and `agents/openai.yaml`.

## Repository Layout

```text
video-transcribe-skill/
  video-transcribe/
    SKILL.md
    agents/openai.yaml
    scripts/transcribe_video.py
  docs/
    index.html
    styles.css
    technical-route.md
  tests/
    test_transcribe_video.py
  requirements.txt
  LICENSE
```

## Install

Clone the repository into your Codex skills folder:

```powershell
cd $env:USERPROFILE\.codex\skills
git clone https://github.com/UKplus8HRS/video-transcribe-skill.git
```

If your Codex skill loader expects one folder per skill directly under `.codex/skills`, copy or symlink `video-transcribe/`:

```powershell
Copy-Item -Recurse .\video-transcribe-skill\video-transcribe .\video-transcribe
```

Install FFmpeg:

```powershell
winget install --id Gyan.FFmpeg --exact --accept-package-agreements --accept-source-agreements --silent
```

Create the local Whisper environment:

```powershell
$venv = "$env:USERPROFILE\.agent-reach\local-whisper-venv"
python -m venv $venv
& "$venv\Scripts\python.exe" -m pip install --upgrade pip
& "$venv\Scripts\python.exe" -m pip install -r .\video-transcribe-skill\requirements.txt
```

## Usage

Run directly:

```powershell
$py = "$env:USERPROFILE\.agent-reach\local-whisper-venv\Scripts\python.exe"
& $py ".\video-transcribe-skill\video-transcribe\scripts\transcribe_video.py" "https://www.bilibili.com/video/BV1hi7w6ME4Q/" --language zh
```

Or invoke it in Codex:

```text
Use $video-transcribe to transcribe and summarize this video link:
https://www.bilibili.com/video/BV1hi7w6ME4Q/
```

## Technical Route

See [docs/technical-route.md](docs/technical-route.md) for the full bilingual architecture and routing explanation.

## Limits

- Bilibili extraction depends on public web APIs and may break if the platform changes.
- Local CPU transcription is slower than cloud transcription.
- Whisper output may contain homophone errors. Use the transcript as evidence, then normalize obvious names in the summary.
- Generic URL support requires `yt-dlp`.

## License

MIT

---

## 中文

> 一个本地 Codex skill，用来把视频链接变成带时间戳的转写文本和摘要。

## 为什么做这个

很多有价值的视频没有字幕，尤其是 B 站上的短教程、演示和实操视频。这个 skill 给 Codex 一条可复用的“看视频”路线：先用确定性工具拿到音频和转写文本，再让模型做摘要、分类、提取和问答。

它不依赖云端转写 API key。

## 功能

- 支持 B 站链接和 BV 号，通过 B 站公开 API 解析。
- 支持 YouTube 和通用视频链接，使用 `yt-dlp` 作为 fallback。
- 支持本地音视频文件。
- 使用本地 `faster-whisper` 在 CPU 上转写。
- 输出带时间戳的 `transcript.txt`。
- 输出 `metadata.json`，记录来源、平台、语言、路径和模型。
- 包含 Codex skill 所需的 `SKILL.md` 和 `agents/openai.yaml`。

## 安装

把仓库克隆到 Codex skills 目录：

```powershell
cd $env:USERPROFILE\.codex\skills
git clone https://github.com/UKplus8HRS/video-transcribe-skill.git
```

如果你的 Codex 需要 skill 文件夹直接位于 `.codex/skills` 下，复制 `video-transcribe/`：

```powershell
Copy-Item -Recurse .\video-transcribe-skill\video-transcribe .\video-transcribe
```

安装 FFmpeg：

```powershell
winget install --id Gyan.FFmpeg --exact --accept-package-agreements --accept-source-agreements --silent
```

创建本地 Whisper 环境：

```powershell
$venv = "$env:USERPROFILE\.agent-reach\local-whisper-venv"
python -m venv $venv
& "$venv\Scripts\python.exe" -m pip install --upgrade pip
& "$venv\Scripts\python.exe" -m pip install -r .\video-transcribe-skill\requirements.txt
```

## 使用

直接运行：

```powershell
$py = "$env:USERPROFILE\.agent-reach\local-whisper-venv\Scripts\python.exe"
& $py ".\video-transcribe-skill\video-transcribe\scripts\transcribe_video.py" "https://www.bilibili.com/video/BV1hi7w6ME4Q/" --language zh
```

在 Codex 里调用：

```text
Use $video-transcribe to transcribe and summarize this video link:
https://www.bilibili.com/video/BV1hi7w6ME4Q/
```

## 技术路线

完整的双语技术路线见 [docs/technical-route.md](docs/technical-route.md)。

## 限制

- B 站音频提取依赖公开 Web API，平台变更可能导致失效。
- 本地 CPU 转写比云端转写慢。
- Whisper 可能产生同音错字，摘要时应根据上下文修正常见专名。
- 通用链接支持需要安装 `yt-dlp`。

## 许可证

MIT
