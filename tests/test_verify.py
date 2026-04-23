from app.verify import verify_downloads
from app.models import ScrapeItem


def test_verify_marks_existing_mp4_true(tmp_path):
    folder = tmp_path / "scraped"
    folder.mkdir()

    (folder / "Alpha.mp4").write_text("x")

    items = [
        ScrapeItem(
            url="https://a.com",
            status="FALSE",
            title="Alpha"
        )
    ]

    stats = verify_downloads(
    items,
    output_dir=str(folder),
    working_dir=str(folder)
)

    assert items[0].status == "TRUE"

    assert stats["changed"] == 1
    assert stats["partial"] == 0
    assert stats["restored"] == 0


def test_verify_marks_segment_folder_partial(tmp_path):
    folder = tmp_path / "scraped"
    folder.mkdir()

    (folder / "Alpha.mp4.segments").mkdir()

    items = [
        ScrapeItem(
            url="https://a.com",
            status="FALSE",
            title="Alpha"
        )
    ]

    stats = verify_downloads(
    items,
    output_dir=str(folder),
    working_dir=str(folder)
)

    assert items[0].status == "PARTIAL"

    assert stats["changed"] == 1
    assert stats["partial"] == 1
    assert stats["restored"] == 0


def test_verify_marks_missing_false(tmp_path):
    folder = tmp_path / "scraped"
    folder.mkdir()

    items = [
        ScrapeItem(
            url="https://a.com",
            status="TRUE",
            title="Alpha"
        )
    ]

    stats = verify_downloads(
    items,
    output_dir=str(folder),
    working_dir=str(folder)
)

    assert items[0].status == "FALSE"

    assert stats["changed"] == 1
    assert stats["partial"] == 0
    assert stats["restored"] == 1


def test_verify_skips_blank_titles(tmp_path):
    folder = tmp_path / "scraped"
    folder.mkdir()

    items = [
        ScrapeItem(
            url="https://a.com",
            status="ERROR",
            title=""
        )
    ]

    stats = verify_downloads(
    items,
    output_dir=str(folder),
    working_dir=str(folder)
)

    assert items[0].status == "ERROR"

    assert stats["changed"] == 0
    assert stats["partial"] == 0
    assert stats["restored"] == 0


def test_verify_no_change_when_already_true_and_file_exists(tmp_path):
    folder = tmp_path / "scraped"
    folder.mkdir()

    (folder / "Alpha.mp4").write_text("x")

    items = [
        ScrapeItem(
            url="https://a.com",
            status="TRUE",
            title="Alpha"
        )
    ]

    stats = verify_downloads(
    items,
    output_dir=str(folder),
    working_dir=str(folder)
)

    assert items[0].status == "TRUE"
    assert stats["changed"] == 0


def test_verify_multiple_items_mixed_results(tmp_path):
    folder = tmp_path / "scraped"
    folder.mkdir()

    (folder / "One.mp4").write_text("x")
    (folder / "Two.mp4.segments").mkdir()

    items = [
        ScrapeItem(url="1", status="FALSE", title="One"),
        ScrapeItem(url="2", status="FALSE", title="Two"),
        ScrapeItem(url="3", status="TRUE", title="Three"),
    ]

    stats = verify_downloads(
    items,
    output_dir=str(folder),
    working_dir=str(folder)
)

    assert items[0].status == "TRUE"
    assert items[1].status == "PARTIAL"
    assert items[2].status == "FALSE"

    assert stats["changed"] == 3
    assert stats["partial"] == 1
    assert stats["restored"] == 1

def test_verify_preserves_error_when_file_missing(tmp_path):
    folder = tmp_path / "scraped"
    folder.mkdir()

    items = [
        ScrapeItem(
            url="https://a.com",
            status="ERROR",
            title="Broken"
        )
    ]

    stats = verify_downloads(
    items,
    output_dir=str(folder),
    working_dir=str(folder)
)

    assert items[0].status == "ERROR"
    assert stats["changed"] == 0
    assert stats["restored"] == 0