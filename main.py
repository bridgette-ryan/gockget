from app.banner import print_welcome
from app.loader import load_scrape_file
from app.utils import clear_errors
from app.verify import verify_downloads
from app.workers import download_scrape_list
from app.saver import save_scrape_file
from app.cli import parse_args
from app.config import FILE_NAME


def main():
    args = parse_args()

    if not args.transphobia:
        print_welcome()

    items, load_stats = load_scrape_file(FILE_NAME)

    if args.clear_errors:
        cleared = clear_errors(items)
        print(f"Cleared {cleared} errored items.")

    # Maintenance mode: verify then exit
    if args.verify:
        verify_stats = verify_downloads(items)

        print(f"{verify_stats['changed']} records updated")
        print(f"{verify_stats['partial']} partial files found")
        print(f"{verify_stats['restored']} missing files reset")

        save_scrape_file(FILE_NAME, items)
        return

    print(f"{load_stats.loaded} unique rows loaded")
    print(f"{load_stats.duplicates} duplicates removed")
    print(f"{load_stats.ready} ready to download")
    print(f"{load_stats.complete} already complete")
    print(f"{load_stats.errors} previous errors")

    try:
        download_scrape_list(
            items,
            max_workers=args.threads,
            retry_errors=args.retry_errors
        )
    finally:
        save_scrape_file(FILE_NAME, items)


if __name__ == "__main__":
    main()