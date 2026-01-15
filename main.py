import argparse
from pathlib import Path
import config as user_config
from src.processor_core import process_posts
from src.cleanup import remove_stale_files
from src.utils import validate_inputs
from src import settings


def main(args):
    settings.init(user_config)
    source_dir, post_dir, img_dir = make_paths()
    if not validate_inputs(source_dir):
        return

    if not args.cleanup:
        process_posts(source_dir, post_dir, img_dir, args.dry, args.layout, args.force)

    if args.update or args.cleanup:
        remove_stale_files(source_dir, post_dir, img_dir)


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
        "-f",
        "--force",
        action="store_true",
        help="Processes every files regardless of change states.",
    )
    parser.add_argument(
        "--layout", default="post", help="Jekyll layout to use (default: post)."
    )

    return parser


def make_paths():
    source_dir = Path(user_config.SOURCE_DIR)
    post_dir, img_dir = [
        Path(user_config.JEKYLL_DIR) / folder
        for folder in (user_config.POST_FOLDER, user_config.IMG_FOLDER)
    ]
    return source_dir, post_dir, img_dir


if __name__ == "__main__":
    parser = setup_parser()
    args = parser.parse_args()

    if args.dry and (args.cleanup or args.update):
        parser.error(
            "--dry cannot be combined with --cleanup or --update. --cleanup and --update have confirmation by default."
        )

    main(args)
