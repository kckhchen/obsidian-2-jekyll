import argparse
from pathlib import Path
from config import *
from processor import build_posts
from cleanup import remove_stale_files
from utils import validate_inputs


def main(args):
    source_dir, img_url_prefix = map(Path, [SOURCE_DIR, IMG_URL_PREFIX])
    post_dest, img_dest, includes_dir = [
        Path(JEKYLL_DIR) / folder
        for folder in (POST_FOLDER, IMG_FOLDER, INCLUDES_FOLDER)
    ]

    if not validate_inputs(source_dir):
        return

    if not args.cleanup:
        build_posts(
            post_dest,
            img_dest,
            img_url_prefix,
            source_dir,
            includes_dir,
            args.layout,
            MATH_RENDERING_MODE,
            args.dry,
        )

    if args.update or args.cleanup:
        remove_stale_files(source_dir, post_dest, img_dest)


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
        help="Update posts and clean up stale posts adn images.",
    )

    parser.add_argument(
        "--dry", action="store_true", help="Dry run: simulate without changes."
    )
    parser.add_argument(
        "--layout", default="post", help="Jekyll layout to use (default: post)."
    )

    return parser


if __name__ == "__main__":
    parser = setup_parser()
    args = parser.parse_args()

    if args.dry and (args.cleanup or args.update):
        parser.error("--dry cannot be combined with --cleanup or --update")

    main(args)
