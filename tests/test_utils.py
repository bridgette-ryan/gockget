from app.utils import clear_errors
from app.models import ScrapeItem
from app.utils import make_safe_title


def test_clear_errors_resets_error_items():
    items = [
        ScrapeItem(
            url="https://a.com",
            status="ERROR",
            title="Broken"
        ),
        ScrapeItem(
            url="https://b.com",
            status="TRUE",
            title="Good"
        ),
    ]

    count = clear_errors(items)

    assert count == 1

    assert items[0].status == "FALSE"
    assert items[0].title == ""

    assert items[1].status == "TRUE"
    assert items[1].title == "Good"


def test_clear_errors_multiple_items():
    items = [
        ScrapeItem(url="1", status="ERROR", title="A"),
        ScrapeItem(url="2", status="ERROR", title="B"),
        ScrapeItem(url="3", status="FALSE", title="C"),
    ]

    count = clear_errors(items)

    assert count == 2

    assert items[0].status == "FALSE"
    assert items[1].status == "FALSE"
    assert items[2].status == "FALSE"

    assert items[0].title == ""
    assert items[1].title == ""
    assert items[2].title == "C"


def test_clear_errors_no_matches():
    items = [
        ScrapeItem(url="1", status="TRUE", title="Done"),
        ScrapeItem(url="2", status="FALSE", title="Queued"),
    ]

    count = clear_errors(items)

    assert count == 0

    assert items[0].status == "TRUE"
    assert items[1].status == "FALSE"

def test_make_safe_title_replaces_invalid_chars():
    result = make_safe_title('Bad<>:"/\\|?*Name')
    assert '<' not in result
    assert '>' not in result
    assert ':' not in result
    assert '/' not in result
    assert '\\' not in result
    assert '|' not in result
    assert '?' not in result
    assert '*' not in result
    assert result == "Bad Name"


def test_make_safe_title_reserved_name():
    result = make_safe_title("CON")
    assert result == "CON_file"


def test_make_safe_title_empty_uses_fallback():
    result = make_safe_title("", "https://a.com")
    assert result.startswith("untitled_")


def test_make_safe_title_trims_trailing_dot_space():
    result = make_safe_title("Hello . ")
    assert result == "Hello"


def test_make_safe_title_limits_length():
    title = "A" * 500
    result = make_safe_title(title)
    assert len(result) <= 180