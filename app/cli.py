import argparse
import sys

def positive_int(value):
    ivalue = int(value)

    if ivalue < 1:
        raise argparse.ArgumentTypeError(
            "threads must be at least 1"
        )

    return ivalue

def parse_args(args=None):
    parser = argparse.ArgumentParser(
        description="Download items from scrape.txt"
    )

    parser.add_argument(
        "--transphobia",
        action="store_true",
        help="Skip the welcome banner"
    )

    parser.add_argument(
        "--threads",
        type=positive_int,
        default=4,
        help="Number of download threads"
    )

    parser.add_argument(
        "--verify",
        action="store_true",
        help="Verify downloaded files against scrape records"
    )

    parser.add_argument(
        "--retry-errors",
        action="store_true",
        help="Retry items currently marked ERROR"
    )

    parser.add_argument(
        "--clear-errors",
        action="store_true",
        help="Reset ERROR items back to FALSE before processing"
    )

    if args is None:
        args = sys.argv[1:]

    return parser.parse_args(args)