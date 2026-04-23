from pathlib import Path

from app.config import OUTPUT_DIR, WORKING_DIR
from app.utils import make_safe_title


def verify_downloads(
    items,
    output_dir=OUTPUT_DIR,
    working_dir=WORKING_DIR
):
    final_base = Path(output_dir)
    working_base = Path(working_dir)

    changed = 0
    partial = 0
    restored = 0

    for item in items:
        if not item.title.strip():
            continue

        safe_title = make_safe_title(item.title, item.url)

        final_file = final_base / f"{safe_title}.mp4"
        segment_dir = working_base / f"{safe_title}.mp4.segments"

        original = item.status

        if final_file.exists():
            item.status = "TRUE"

        elif segment_dir.exists() and segment_dir.is_dir():
            item.status = "PARTIAL"
            partial += 1

        else:
            if item.status in {"TRUE", "PARTIAL"}:
                item.status = "FALSE"
                restored += 1

        if item.status != original:
            changed += 1

    return {
        "changed": changed,
        "partial": partial,
        "restored": restored,
    }