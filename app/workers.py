from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import time
import random
from app.config import WORKING_DIR

from app.models import ScrapeItem
from app.downloader import download_video





def download_scrape_list(
    items: List[ScrapeItem],
    max_workers: int = 4,
    retry_errors: bool = False
) -> None:

    def worker(item: ScrapeItem):
        title = download_video(item)
        return item, title

    allowed = {"FALSE", "PARTIAL"}

    if retry_errors:
        allowed.add("ERROR")

    pending_items = [
        item for item in items
        if item.status in allowed
    ]

    if not pending_items:
        print("No pending downloads.")
        return

    print(f"{len(pending_items)} item(s) queued with {max_workers} thread(s).")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {
            executor.submit(worker, item): item
            for item in pending_items
        }

        for future in as_completed(future_map):
            item = future_map[future]

            try:
                _, title = future.result()

                item.status = "TRUE"
                item.title = title

                print(f"[SUCCESS] {item.url} -> {title}")

            except Exception as ex:
                segment_dir = (
                    Path(WORKING_DIR) /
                    f"{item.safe_title}.mp4.segments"
                )

                if item.safe_title and segment_dir.exists() and segment_dir.is_dir():
                    item.status = "PARTIAL"
                else:
                    item.status = "ERROR"

                print(f"[FAILED] {item.url} -> {str(ex)}")

            delay = random.uniform(2, 4)
            time.sleep(delay)