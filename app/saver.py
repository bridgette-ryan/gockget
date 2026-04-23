from app.models import ScrapeItem
from pathlib import Path
from typing import List

# ----------------------------
# Save File
# ----------------------------

def save_scrape_file(file_path: str, items: List[ScrapeItem]) -> None:
    """
    Writes the scrape list back to disk.

    Output format:
    URL | SCRAPED | TITLE
    """

    path = Path(file_path)

    with path.open("w", encoding="utf-8", newline="") as file:
        file.write("URL | SCRAPED | TITLE\n")

        for item in items:
            line = f"{item.url} | {item.status} | {item.title}\n"
            file.write(line)
