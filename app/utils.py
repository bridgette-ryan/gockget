import re
import hashlib


def make_safe_title(title: str, fallback_source: str = "") -> str:
    """
    Convert a title into a filesystem-safe filename.
    Safe for Windows/macOS/Linux.
    """

    title = title.strip()

    # Replace invalid filename chars
    title = re.sub(r'[<>:"/\\|?*]', "-", title)

    # Remove control chars
    title = re.sub(r'[\x00-\x1f]', "", title)

    # Collapse repeated spaces / dashes
    title = re.sub(r"[-\s]+", " ", title).strip()

    # Remove trailing dots/spaces
    title = title.rstrip(" .")

    # Reserved Windows names
    reserved = {
        "CON", "PRN", "AUX", "NUL",
        *(f"COM{i}" for i in range(1, 10)),
        *(f"LPT{i}" for i in range(1, 10)),
    }

    if title.upper() in reserved:
        title = f"{title}_file"

    # Empty fallback
    if not title:
        digest = hashlib.sha1(
            fallback_source.encode("utf-8")
        ).hexdigest()[:8]
        title = f"untitled_{digest}"

    # Limit length
    title = title[:180].rstrip()

    return title

def clear_errors(items):
    count = 0

    for item in items:
        if item.status == "ERROR":
            item.status = "FALSE"
            item.title = ""
            count += 1

    return count