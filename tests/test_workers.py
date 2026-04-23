from app.workers import download_scrape_list
from app.models import ScrapeItem


def test_workers_only_process_false_items(monkeypatch):
    called = []

    def fake_download(item):
        called.append(item.url)
        return "Downloaded Title"

    monkeypatch.setattr(
        "app.workers.download_video",
        fake_download
    )

    monkeypatch.setattr(
        "app.workers.time.sleep",
        lambda _: None
    )

    monkeypatch.setattr(
        "app.workers.random.uniform",
        lambda a, b: 0
    )

    items = [
        ScrapeItem(url="https://a.com", status="FALSE"),
        ScrapeItem(url="https://b.com", status="TRUE"),
        ScrapeItem(url="https://c.com", status="ERROR"),
    ]

    download_scrape_list(items, max_workers=2)

    assert called == ["https://a.com"]

    assert items[0].status == "TRUE"
    assert items[0].title == "Downloaded Title"

    assert items[1].status == "TRUE"
    assert items[2].status == "ERROR"


def test_workers_retry_errors_processes_error_items(monkeypatch):
    called = []

    def fake_download(item):
        called.append(item.url)
        return "Recovered"

    monkeypatch.setattr(
        "app.workers.download_video",
        fake_download
    )

    monkeypatch.setattr(
        "app.workers.time.sleep",
        lambda _: None
    )

    monkeypatch.setattr(
        "app.workers.random.uniform",
        lambda a, b: 0
    )

    items = [
        ScrapeItem(url="https://bad.com", status="ERROR")
    ]

    download_scrape_list(
        items,
        max_workers=1,
        retry_errors=True
    )

    assert called == ["https://bad.com"]
    assert items[0].status == "TRUE"
    assert items[0].title == "Recovered"


def test_workers_marks_failures_as_error(monkeypatch):
    def fake_download(item):
        raise Exception("Boom")

    monkeypatch.setattr(
        "app.workers.download_video",
        fake_download
    )

    monkeypatch.setattr(
        "app.workers.time.sleep",
        lambda _: None
    )

    monkeypatch.setattr(
        "app.workers.random.uniform",
        lambda a, b: 0
    )

    items = [
        ScrapeItem(url="https://fail.com", status="FALSE")
    ]

    download_scrape_list(items, max_workers=1)

    assert items[0].status == "ERROR"


def test_workers_multiple_successes(monkeypatch):
    def fake_download(item):
        return f"title for {item.url}"

    monkeypatch.setattr(
        "app.workers.download_video",
        fake_download
    )

    monkeypatch.setattr(
        "app.workers.time.sleep",
        lambda _: None
    )

    monkeypatch.setattr(
        "app.workers.random.uniform",
        lambda a, b: 0
    )

    items = [
        ScrapeItem(url="https://1.com", status="FALSE"),
        ScrapeItem(url="https://2.com", status="FALSE"),
    ]

    download_scrape_list(items, max_workers=2)

    assert items[0].status == "TRUE"
    assert items[1].status == "TRUE"

    assert "title for" in items[0].title
    assert "title for" in items[1].title


def test_workers_no_pending_items(monkeypatch):
    called = []

    def fake_download(item):
        called.append(item.url)
        return "nope"

    monkeypatch.setattr(
        "app.workers.download_video",
        fake_download
    )

    items = [
        ScrapeItem(url="https://done.com", status="TRUE")
    ]

    download_scrape_list(items)

    assert called == []

def test_workers_marks_failure_as_partial_when_segments_exist(
    monkeypatch,
    tmp_path
):
    def fake_download(item):
        raise Exception("Interrupted")

    monkeypatch.setattr(
        "app.workers.download_video",
        fake_download
    )

    monkeypatch.setattr(
        "app.workers.time.sleep",
        lambda _: None
    )

    monkeypatch.setattr(
        "app.workers.random.uniform",
        lambda a, b: 0
    )

    monkeypatch.chdir(tmp_path)

    segments = (
        tmp_path /
        "scraping" /
        "Broken.mp4.segments"
    )

    segments.mkdir(parents=True)

    items = [
        ScrapeItem(
            url="https://a.com",
            status="FALSE",
            title="Broken",
            safe_title="Broken"
        )
    ]

    download_scrape_list(items, max_workers=1)

    assert items[0].status == "PARTIAL"