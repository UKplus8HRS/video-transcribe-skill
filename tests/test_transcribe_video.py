import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "video-transcribe" / "scripts" / "transcribe_video.py"


def load_module():
    spec = importlib.util.spec_from_file_location("transcribe_video", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_safe_slug_keeps_stable_ascii_parts():
    module = load_module()
    assert module.safe_slug("https://www.bilibili.com/video/BV1hi7w6ME4Q/") == "https-www.bilibili.com-video-BV1hi7w6ME4Q"


def test_safe_slug_has_fallback_for_non_ascii():
    module = load_module()
    assert module.safe_slug("中文视频") == "video"
