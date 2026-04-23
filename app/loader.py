from pathlib import Path
from app.models import LoadStats, ScrapeItem

# ----------------------------
# Loader
# ----------------------------

def load_scrape_file(file_path: str):
    items = []
    seen_urls = set()
    stats = LoadStats()

    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        lines = file.readlines()

    for raw_line in lines[1:]:
        line = raw_line.strip()

        if not line:
            continue

        stats.total_rows += 1

        parts = [p.strip() for p in line.split("|")]

        url = parts[0]

        if url in seen_urls:
            stats.duplicates += 1
            continue

        seen_urls.add(url)

        status = parts[1].upper() if len(parts) >= 2 and parts[1] else "FALSE"
        title = parts[2] if len(parts) >= 3 else ""

        item = ScrapeItem(url=url, status=status, title=title)
        items.append(item)

        stats.loaded += 1

        if status == "FALSE":
            stats.ready += 1
        elif status == "TRUE":
            stats.complete += 1
        elif status == "ERROR":
            stats.errors += 1

    return items, stats