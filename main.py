import argparse

from src.cleanup import remove_stale_files
from src.config import VAULT_DIR, POST_DIR, IMG_DIR
from src.fs_ops import ensure_css_exists, setup_dir
from src.processor_core import process_posts
from src.utils import get_valid_files


def main(args):
    valid_files = get_valid_files(VAULT_DIR, POST_DIR)

    if not args.cleanup:
        if args.dry:
            print("------------ DRY RUN MODE -------------")
            print("Operations will be printed but files won't be changed.\n")

        print(f"Start processing posts in Vault [ {VAULT_DIR} ]...")
        print(f"Destination path: [ {POST_DIR} ]\n")

        setup_dir([POST_DIR, IMG_DIR], args.dry)
        ensure_css_exists("obsidian-callouts.html", args.dry)
        process_posts(
            valid_files,
            args.dry,
            args.layout,
            args.force,
            args.only,
        )

    if args.update or args.cleanup:
        remove_stale_files(valid_files, POST_DIR, IMG_DIR)


def setup_parser():
    parser = argparse.ArgumentParser(description="Convert Obsidian notes to Jekyll")

    action_group = parser.add_mutually_exclusive_group()
    action_group.add_argument(
        "-c", "--cleanup", action="store_true", help="Clean up stale posts and images."
    )
    action_group.add_argument(
        "-u",
        "--update",
        action="store_true",
        help="Update posts and clean up stale posts and images.",
    )

    parser.add_argument(
        "--dry", action="store_true", help="Dry run: simulate without changes."
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Processes every file regardless of change states.",
    )
    parser.add_argument(
        "--layout",
        type=str,
        default="post",
        help="Jekyll layout to use (default: post).",
    )
    parser.add_argument("--only", default=None, help="Only process the selected post.")

    return parser


if __name__ == "__main__":
    parser = setup_parser()
    args = parser.parse_args()

    if args.dry and (args.cleanup or args.update):
        parser.error("--dry cannot be combined with --cleanup or --update.")

    if args.only and (args.cleanup or args.update):
        parser.error("--only cannot be combined with --cleanup or --update.")

    main(args)
