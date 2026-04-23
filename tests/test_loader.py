from app.loader import load_scrape_file


def test_load_basic_file(tmp_path):
    file = tmp_path / "scrape.txt"

    file.write_text(
        "URL | SCRAPED | TITLE\n"
        "https://a.com | FALSE | Alpha\n"
        "https://b.com | TRUE | Beta\n",
        encoding="utf-8"
    )

    items, stats = load_scrape_file(str(file))

    assert len(items) == 2

    assert items[0].url == "https://a.com"
    assert items[0].status == "FALSE"
    assert items[0].title == "Alpha"

    assert items[1].url == "https://b.com"
    assert items[1].status == "TRUE"
    assert items[1].title == "Beta"

    assert stats.total_rows == 2
    assert stats.loaded == 2
    assert stats.ready == 1
    assert stats.complete == 1
    assert stats.errors == 0
    assert stats.duplicates == 0


def test_load_skips_duplicates(tmp_path):
    file = tmp_path / "scrape.txt"

    file.write_text(
        "URL | SCRAPED | TITLE\n"
        "https://a.com | FALSE |\n"
        "https://a.com | TRUE | Duplicate\n",
        encoding="utf-8"
    )

    items, stats = load_scrape_file(str(file))

    assert len(items) == 1
    assert items[0].url == "https://a.com"

    assert stats.total_rows == 2
    assert stats.loaded == 1
    assert stats.duplicates == 1
    assert stats.ready == 1


def test_missing_status_defaults_false(tmp_path):
    file = tmp_path / "scrape.txt"

    file.write_text(
        "URL | SCRAPED | TITLE\n"
        "https://a.com\n",
        encoding="utf-8"
    )

    items, stats = load_scrape_file(str(file))

    assert len(items) == 1
    assert items[0].status == "FALSE"

    assert stats.ready == 1
    assert stats.loaded == 1


def test_error_rows_counted(tmp_path):
    file = tmp_path / "scrape.txt"

    file.write_text(
        "URL | SCRAPED | TITLE\n"
        "https://a.com | ERROR | Broken\n",
        encoding="utf-8"
    )

    items, stats = load_scrape_file(str(file))

    assert len(items) == 1
    assert items[0].status == "ERROR"

    assert stats.errors == 1
    assert stats.ready == 0
    assert stats.complete == 0


def test_blank_lines_ignored(tmp_path):
    file = tmp_path / "scrape.txt"

    file.write_text(
        "URL | SCRAPED | TITLE\n"
        "\n"
        "https://a.com | FALSE |\n"
        "\n",
        encoding="utf-8"
    )

    items, stats = load_scrape_file(str(file))

    assert len(items) == 1
    assert stats.total_rows == 1