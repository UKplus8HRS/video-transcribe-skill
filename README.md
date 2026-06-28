# Video Transcribe Skill

> Offline-first, lightweight Codex skill for turning video links into timestamped transcripts and summaries.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Skill](https://img.shields.io/badge/Codex-SKILL.md-0b6b57.svg)](video-transcribe/SKILL.md)
[![Offline first](https://img.shields.io/badge/offline--first-local%20Whisper-c84f31.svg)](#why)
[![No backend](https://img.shields.io/badge/no%20backend-no%20hosted%20service-555.svg)](#project-stance)

English | [中文](#中文)

## TL;DR

```powershell
git clone https://github.com/UKplus8HRS/video-transcribe-skill.git
winget install --id Gyan.FFmpeg --exact
pip install -r .\video-transcribe-skill\requirements.txt
```

macOS/Linux:

```bash
git clone https://github.com/UKplus8HRS/video-transcribe-skill.git
brew install ffmpeg   # macOS; use apt/dnf/pacman on Linux
pip install -r ./video-transcribe-skill/requirements.txt
```

Then ask Codex:

```text
Use $video-transcribe to transcribe and summarize this video link:
https://www.bilibili.com/video/BV1hi7w6ME4Q/
```

## Why

Many useful videos have no subtitles, especially short Bilibili demos and tutorials. This skill gives Codex a repeatable path to "watch" those videos by using deterministic tooling first:

1. resolve the video source,
2. extract the audio,
3. normalize it with FFmpeg,
4. transcribe it locally with faster-whisper,
5. let the model summarize or extract answers from the transcript.

No cloud transcription key is required.

## Project stance

This is intentionally small:

- offline-first local transcription, not a hosted transcription service;
- no custom backend, account system, queue, dashboard, or `.io` product layer;
- README-first documentation, with GitHub Pages only as a lightweight visual mirror;
- deterministic code handles routing and audio processing; the model only reads the transcript.

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

Clone the repository:

```powershell
git clone https://github.com/UKplus8HRS/video-transcribe-skill.git
```

Install the skill folder.

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse .\video-transcribe-skill\video-transcribe "$env:USERPROFILE\.codex\skills\video-transcribe"
```

macOS/Linux:

```bash
mkdir -p ~/.codex/skills
cp -R ./video-transcribe-skill/video-transcribe ~/.codex/skills/video-transcribe
```

Install FFmpeg.

Windows:

```powershell
winget install --id Gyan.FFmpeg --exact --accept-package-agreements --accept-source-agreements --silent
```

macOS:

```bash
brew install ffmpeg
```

Linux:

```bash
sudo apt-get update && sudo apt-get install -y ffmpeg
```

Create the local Whisper environment.

Windows:

```powershell
$venv = "$env:USERPROFILE\.agent-reach\local-whisper-venv"
python -m venv $venv
& "$venv\Scripts\python.exe" -m pip install --upgrade pip
& "$venv\Scripts\python.exe" -m pip install -r .\video-transcribe-skill\requirements.txt
```

macOS/Linux:

```bash
python3 -m venv ~/.agent-reach/local-whisper-venv
~/.agent-reach/local-whisper-venv/bin/python -m pip install --upgrade pip
~/.agent-reach/local-whisper-venv/bin/python -m pip install -r ./video-transcribe-skill/requirements.txt
```

## Usage

Run directly.

Windows:

```powershell
$py = "$env:USERPROFILE\.agent-reach\local-whisper-venv\Scripts\python.exe"
& $py ".\video-transcribe-skill\video-transcribe\scripts\transcribe_video.py" "https://www.bilibili.com/video/BV1hi7w6ME4Q/" --language zh
```

macOS/Linux:

```bash
~/.agent-reach/local-whisper-venv/bin/python \
  ./video-transcribe-skill/video-transcribe/scripts/transcribe_video.py \
  "https://www.bilibili.com/video/BV1hi7w6ME4Q/" \
  --language zh
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

> 一个离线优先、轻量的 Codex skill，用来把视频链接变成带时间戳的转写文本和摘要。

## 一句话

这不是托管转写服务，也不需要自建后端。它只是一个可以放进 Codex skills 目录的本地小工具：抓音频、转码、本地 Whisper 转写，然后让 Codex 基于转写文本总结。

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

如果你的 Codex 需要 skill 文件夹直接位于 `.codex/skills` 下，复制 `video-transcribe/`。

Windows PowerShell：

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse .\video-transcribe-skill\video-transcribe "$env:USERPROFILE\.codex\skills\video-transcribe"
```

macOS/Linux：

```bash
mkdir -p ~/.codex/skills
cp -R ./video-transcribe-skill/video-transcribe ~/.codex/skills/video-transcribe
```

安装 FFmpeg：

```powershell
winget install --id Gyan.FFmpeg --exact --accept-package-agreements --accept-source-agreements --silent
```

macOS：

```bash
brew install ffmpeg
```

Linux：

```bash
sudo apt-get update && sudo apt-get install -y ffmpeg
```

创建本地 Whisper 环境：

```powershell
$venv = "$env:USERPROFILE\.agent-reach\local-whisper-venv"
python -m venv $venv
& "$venv\Scripts\python.exe" -m pip install --upgrade pip
& "$venv\Scripts\python.exe" -m pip install -r .\video-transcribe-skill\requirements.txt
```

macOS/Linux：

```bash
python3 -m venv ~/.agent-reach/local-whisper-venv
~/.agent-reach/local-whisper-venv/bin/python -m pip install --upgrade pip
~/.agent-reach/local-whisper-venv/bin/python -m pip install -r ./video-transcribe-skill/requirements.txt
```

## 使用

直接运行。

Windows：

```powershell
$py = "$env:USERPROFILE\.agent-reach\local-whisper-venv\Scripts\python.exe"
& $py ".\video-transcribe-skill\video-transcribe\scripts\transcribe_video.py" "https://www.bilibili.com/video/BV1hi7w6ME4Q/" --language zh
```

macOS/Linux：

```bash
~/.agent-reach/local-whisper-venv/bin/python \
  ./video-transcribe-skill/video-transcribe/scripts/transcribe_video.py \
  "https://www.bilibili.com/video/BV1hi7w6ME4Q/" \
  --language zh
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
