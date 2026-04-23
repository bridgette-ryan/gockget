import shutil
import hashlib

from pathlib import Path
from xnxx_api import Client

from app.config import OUTPUT_DIR, WORKING_DIR
from app.exceptions import VideoDownloadError
from app.models import ScrapeItem


def download_video(
    item: ScrapeItem,
    output_dir: str = OUTPUT_DIR,
    working_dir: str = WORKING_DIR
) -> str:
    """
    Downloads into working_dir first.
    Moves completed file into output_dir after verification.
    """

    final_path = Path(output_dir)
    working_path = Path(working_dir)

    final_path.mkdir(parents=True, exist_ok=True)
    working_path.mkdir(parents=True, exist_ok=True)

    client = Client()

    try:
        video = client.get_video(item.url)

        if video is None:
            raise VideoDownloadError(
                f"Metadata lookup returned no result for {item.url}"
            )

        title = getattr(video, "title", "").strip()

        if not title:
            existing = item.title.strip()

            if existing:
                title = existing
            else:
                digest = hashlib.sha1(
                    item.url.encode("utf-8")
                ).hexdigest()[:8]

                title = f"untitled_video_{digest}"

        if item.title.strip():
            title = item.title.strip()

        safe_title = (
            title
            .replace("/", "-")
            .replace("\\", "-")
            .replace(":", "-")
            .strip()
        )

        # NEW: store both values on item immediately
        item.title = title
        item.safe_title = safe_title

        state_file = working_path / f"{safe_title}.state.json"

        report = video.download(
            quality="best",
            path=str(working_path),
            remux=True,
            return_report=True,
            cleanup_on_stop=False,
            segment_state_path=str(state_file),
        )

        if report is None:
            raise VideoDownloadError("Download produced no report")

        if report.get("cancelled"):
            raise VideoDownloadError("Download cancelled")

        if report.get("error"):
            raise VideoDownloadError(str(report["error"]))

        working_file = working_path / f"{safe_title}.mp4"
        segment_dir = working_path / f"{safe_title}.mp4.segments"

        if not working_file.exists():
            raise VideoDownloadError(
                f"Incomplete download: final file missing for {title}"
            )

        if segment_dir.exists() and segment_dir.is_dir():
            raise VideoDownloadError(
                f"Incomplete download: segments remain for {title}"
            )

        final_file = final_path / f"{safe_title}.mp4"

        shutil.move(str(working_file), str(final_file))

        return title

    except VideoDownloadError:
        raise

    except Exception as ex:
        raise VideoDownloadError(
            f"Unexpected failure downloading {item.url}: {str(ex)}"
        ) from ex