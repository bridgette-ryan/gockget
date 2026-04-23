import pytest
from app.requirements import _clean_package_name, _package_to_import_name, check_requirements


# -------------------------------------------------
# Helper Function Tests
# -------------------------------------------------

def test_clean_package_name_basic():
    assert _clean_package_name("xnxx_api") == "xnxx_api"


def test_clean_package_name_with_version():
    assert _clean_package_name("pytest>=8.0") == "pytest"


def test_clean_package_name_with_extras():
    assert _clean_package_name("httpx[http2]") == "httpx"


def test_clean_package_name_comment():
    assert _clean_package_name("# comment") == ""


def test_package_mapping():
    assert _package_to_import_name("beautifulsoup4") == "bs4"
    assert _package_to_import_name("pillow") == "PIL"
    assert _package_to_import_name("pytest") == "pytest"


# -------------------------------------------------
# Main Requirements Tests
# -------------------------------------------------

def test_check_requirements_passes(tmp_path, monkeypatch):
    file = tmp_path / "requirements.txt"
    file.write_text(
        "pytest\nhttpx[http2]\n",
        encoding="utf-8"
    )

    monkeypatch.setattr(
        "importlib.util.find_spec",
        lambda name: object()
    )

    check_requirements(str(file))


def test_check_requirements_fails_when_missing(tmp_path, monkeypatch):
    file = tmp_path / "requirements.txt"
    file.write_text(
        "pytest\nmissing_package\n",
        encoding="utf-8"
    )

    def fake_find_spec(name):
        if name == "missing_package":
            return None
        return object()

    monkeypatch.setattr(
        "importlib.util.find_spec",
        fake_find_spec
    )

    with pytest.raises(SystemExit):
        check_requirements(str(file))

def test_check_requirements_missing_file(tmp_path, capsys):
    file = tmp_path / "does_not_exist.txt"

    check_requirements(str(file))

    captured = capsys.readouterr()

    assert "requirements.txt not found." in captured.out


def test_check_requirements_prints_install_hint(tmp_path, monkeypatch, capsys):
    file = tmp_path / "requirements.txt"

    file.write_text(
        "missing_package\n",
        encoding="utf-8"
    )

    monkeypatch.setattr(
        "importlib.util.find_spec",
        lambda name: None
    )

    with pytest.raises(SystemExit):
        check_requirements(str(file))

    captured = capsys.readouterr()

    assert "Missing required packages:" in captured.out
    assert "missing_package" in captured.out
    assert "pip install -r requirements.txt" in captured.out

def test_check_requirements_multiple_missing_packages(
    tmp_path,
    monkeypatch,
    capsys
):
    file = tmp_path / "requirements.txt"

    file.write_text(
        "missing_one\nmissing_two\n",
        encoding="utf-8"
    )

    monkeypatch.setattr(
        "importlib.util.find_spec",
        lambda name: None
    )

    with pytest.raises(SystemExit):
        check_requirements(str(file))

    captured = capsys.readouterr()

    assert " - missing_one" in captured.out
    assert " - missing_two" in captured.out

def test_check_requirements_calls_sys_exit(tmp_path, monkeypatch):
    file = tmp_path / "requirements.txt"

    file.write_text(
        "missing_package\n",
        encoding="utf-8"
    )

    monkeypatch.setattr(
        "importlib.util.find_spec",
        lambda name: None
    )

    called = {}

    def fake_exit(code):
        called["code"] = code
        raise SystemExit(code)

    monkeypatch.setattr(
        "sys.exit",
        fake_exit
    )

    with pytest.raises(SystemExit):
        check_requirements(str(file))

    assert called["code"] == 1

def test_check_requirements_skips_blank_and_comment_lines(
    tmp_path,
    monkeypatch
):
    file = tmp_path / "requirements.txt"

    file.write_text(
        "\n"
        "# comment line\n"
        "pytest\n",
        encoding="utf-8"
    )

    called = []

    def fake_find_spec(name):
        called.append(name)
        return object()

    monkeypatch.setattr(
        "importlib.util.find_spec",
        fake_find_spec
    )

    check_requirements(str(file))

    assert called == ["pytest"]