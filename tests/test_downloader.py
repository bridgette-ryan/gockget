from pathlib import Path

import pytest

from app.downloader import download_video
from app.models import ScrapeItem
from app.exceptions import VideoDownloadError

def test_download_video_success(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)

    class FakeVideo:
        title = "Alpha"

        def download(self, **kwargs):
            # simulate completed file
            (tmp_path / "scraping" / "Alpha.mp4").write_text("x")
            return {}

    class FakeClient:
        def get_video(self, url):
            return FakeVideo()

    monkeypatch.setattr(
        "app.downloader.Client",
        lambda: FakeClient()
    )

    item = ScrapeItem(url="https://a.com")

    title = download_video(item)

    assert title == "Alpha"
    assert (tmp_path / "scraped" / "Alpha.mp4").exists()

def test_download_video_metadata_none(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)

    class FakeClient:
        def get_video(self, url):
            return None

    monkeypatch.setattr(
        "app.downloader.Client",
        lambda: FakeClient()
    )

    item = ScrapeItem(url="https://a.com")

    with pytest.raises(VideoDownloadError):
        download_video(item)

def test_download_video_cancelled(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)

    class FakeVideo:
        title = "Alpha"

        def download(self, **kwargs):
            return {"cancelled": True}

    class FakeClient:
        def get_video(self, url):
            return FakeVideo()

    monkeypatch.setattr(
        "app.downloader.Client",
        lambda: FakeClient()
    )

    with pytest.raises(VideoDownloadError):
        download_video(ScrapeItem(url="x"))

def test_download_video_report_error(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)

    class FakeVideo:
        title = "Alpha"

        def download(self, **kwargs):
            return {"error": "Boom"}

    class FakeClient:
        def get_video(self, url):
            return FakeVideo()

    monkeypatch.setattr(
        "app.downloader.Client",
        lambda: FakeClient()
    )

    with pytest.raises(VideoDownloadError):
        download_video(ScrapeItem(url="x"))

def test_download_video_missing_output(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)

    class FakeVideo:
        title = "Alpha"

        def download(self, **kwargs):
            return {}

    class FakeClient:
        def get_video(self, url):
            return FakeVideo()

    monkeypatch.setattr(
        "app.downloader.Client",
        lambda: FakeClient()
    )

    with pytest.raises(VideoDownloadError):
        download_video(ScrapeItem(url="x"))

def test_download_video_sanitizes_title(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)

    class FakeVideo:
        title = "Bad:/\\Name"

        def download(self, **kwargs):
            (tmp_path / "scraping" / "Bad---Name.mp4").write_text("x")
            return {}

    class FakeClient:
        def get_video(self, url):
            return FakeVideo()

    monkeypatch.setattr(
        "app.downloader.Client",
        lambda: FakeClient()
    )

    title = download_video(ScrapeItem(url="x"))

    assert title == "Bad:/\\Name"
    assert (tmp_path / "scraped" / "Bad---Name.mp4").exists()

def test_download_video_uses_unique_untitled_when_no_titles(
    monkeypatch,
    tmp_path
):
    monkeypatch.chdir(tmp_path)

    class FakeVideo:
        title = ""

        def download(self, **kwargs):
            # derive filename from state path:
            # scraping/untitled_video_xxxxxxxx.state.json
            state_path = Path(kwargs["segment_state_path"])
            stem = state_path.name.replace(".state.json", "")

            mp4_file = tmp_path / "scraping" / f"{stem}.mp4"
            mp4_file.write_text("x")

            return {}

    class FakeClient:
        def get_video(self, url):
            return FakeVideo()

    monkeypatch.setattr(
        "app.downloader.Client",
        lambda: FakeClient()
    )

    item = ScrapeItem(url="https://example.com/video/123")

    title = download_video(item)

    assert title.startswith("untitled_video_")
    assert item.safe_title.startswith("untitled_video_")
    assert (tmp_path / "scraped" / f"{item.safe_title}.mp4").exists()

def test_download_video_reuses_existing_title_when_metadata_blank(
    monkeypatch,
    tmp_path
):
    monkeypatch.chdir(tmp_path)

    class FakeVideo:
        title = ""

        def download(self, **kwargs):
            (tmp_path / "scraping" / "Saved.mp4").write_text("x")
            return {}

    class FakeClient:
        def get_video(self, url):
            return FakeVideo()

    monkeypatch.setattr("app.downloader.Client", lambda: FakeClient())

    item = ScrapeItem(url="x", title="Saved")

    title = download_video(item)

    assert title == "Saved"

def test_download_video_report_error_exact(
    monkeypatch,
    tmp_path
):
    monkeypatch.chdir(tmp_path)

    class FakeVideo:
        title = "Alpha"

        def download(self, **kwargs):
            return {"error": "Boom"}

    class FakeClient:
        def get_video(self, url):
            return FakeVideo()

    monkeypatch.setattr("app.downloader.Client", lambda: FakeClient())

    with pytest.raises(VideoDownloadError) as ex:
        download_video(ScrapeItem(url="x"))

    assert "Boom" in str(ex.value)

def test_download_video_detects_remaining_segments(
    monkeypatch,
    tmp_path
):
    monkeypatch.chdir(tmp_path)

    class FakeVideo:
        title = "Alpha"

        def download(self, **kwargs):
            (tmp_path / "scraping" / "Alpha.mp4").write_text("x")
            (tmp_path / "scraping" / "Alpha.mp4.segments").mkdir()
            return {}

    class FakeClient:
        def get_video(self, url):
            return FakeVideo()

    monkeypatch.setattr("app.downloader.Client", lambda: FakeClient())

    with pytest.raises(VideoDownloadError):
        download_video(ScrapeItem(url="x"))

def test_download_video_wraps_unexpected_error(
    monkeypatch,
    tmp_path
):
    monkeypatch.chdir(tmp_path)

    class FakeClient:
        def get_video(self, url):
            raise RuntimeError("kaboom")

    monkeypatch.setattr("app.downloader.Client", lambda: FakeClient())

    with pytest.raises(VideoDownloadError) as ex:
        download_video(ScrapeItem(url="x"))

    assert "Unexpected failure downloading" in str(ex.value)

def test_download_video_report_error_hits_exact_line(
    monkeypatch,
    tmp_path
):
    monkeypatch.chdir(tmp_path)

    class FakeVideo:
        title = "Alpha"

        def download(self, **kwargs):
            return {"error": "Specific failure"}

    class FakeClient:
        def get_video(self, url):
            return FakeVideo()

    monkeypatch.setattr(
        "app.downloader.Client",
        lambda: FakeClient()
    )

    with pytest.raises(VideoDownloadError) as ex:
        download_video(ScrapeItem(url="https://x.com"))

    assert str(ex.value) == "Specific failure"