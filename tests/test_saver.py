from app.saver import save_scrape_file
from app.models import ScrapeItem


def test_save_creates_expected_file(tmp_path):
    file = tmp_path / "scrape.txt"

    items = [
        ScrapeItem(
            url="https://a.com",
            status="FALSE",
            title=""
        ),
        ScrapeItem(
            url="https://b.com",
            status="TRUE",
            title="Test Title"
        ),
        ScrapeItem(
            url="https://c.com",
            status="ERROR",
            title="Failed Item"
        ),
    ]

    save_scrape_file(str(file), items)

    content = file.read_text(encoding="utf-8")

    expected = (
        "URL | SCRAPED | TITLE\n"
        "https://a.com | FALSE | \n"
        "https://b.com | TRUE | Test Title\n"
        "https://c.com | ERROR | Failed Item\n"
    )

    assert content == expected


def test_save_empty_list_writes_header_only(tmp_path):
    file = tmp_path / "scrape.txt"

    save_scrape_file(str(file), [])

    content = file.read_text(encoding="utf-8")

    assert content == "URL | SCRAPED | TITLE\n"


def test_save_overwrites_existing_file(tmp_path):
    file = tmp_path / "scrape.txt"

    file.write_text("old junk", encoding="utf-8")

    items = [
        ScrapeItem(
            url="https://new.com",
            status="TRUE",
            title="Fresh"
        )
    ]

    save_scrape_file(str(file), items)

    content = file.read_text(encoding="utf-8")

    assert content == (
        "URL | SCRAPED | TITLE\n"
        "https://new.com | TRUE | Fresh\n"
    )


def test_save_preserves_order(tmp_path):
    file = tmp_path / "scrape.txt"

    items = [
        ScrapeItem(url="https://1.com", status="FALSE", title="One"),
        ScrapeItem(url="https://2.com", status="TRUE", title="Two"),
        ScrapeItem(url="https://3.com", status="ERROR", title="Three"),
    ]

    save_scrape_file(str(file), items)

    lines = file.read_text(encoding="utf-8").splitlines()

    assert lines[1].startswith("https://1.com")
    assert lines[2].startswith("https://2.com")
    assert lines[3].startswith("https://3.com")