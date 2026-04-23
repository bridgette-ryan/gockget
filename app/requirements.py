import importlib.util
import re
import sys
from pathlib import Path


def _clean_package_name(line: str) -> str:
    """
    Converts requirement lines into probable import names.
    """

    line = line.strip()

    if not line or line.startswith("#"):
        return ""

    # remove version pins
    line = re.split(r"[<>=!~]", line)[0].strip()

    # remove extras: httpx[http2] -> httpx
    line = re.sub(r"\[.*?\]", "", line)

    return line


def _package_to_import_name(name: str) -> str:
    """
    Handle package/import mismatches.
    """

    mapping = {
        "beautifulsoup4": "bs4",
        "pillow": "PIL",
        "pytest-cov": "pytest_cov",
    }

    return mapping.get(name.lower(), name)


def check_requirements(file_name: str = "requirements.txt") -> None:
    """
    Verifies packages in requirements.txt are installed.
    Exits if missing packages found.
    """

    path = Path(file_name)

    if not path.exists():
        print("requirements.txt not found.")
        return

    missing = []

    for line in path.read_text(encoding="utf-8").splitlines():
        package = _clean_package_name(line)

        if not package:
            continue

        module_name = _package_to_import_name(package)

        if importlib.util.find_spec(module_name) is None:
            missing.append(package)

    if missing:
        print("Missing required packages:")
        for pkg in missing:
            print(f" - {pkg}")

        print("\nInstall them with:")
        print("pip install -r requirements.txt")
        sys.exit(1)