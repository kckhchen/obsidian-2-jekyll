import os
import argparse
from pathlib import Path
from config import *
from processor import build_posts
from cleanup import remove_stale_files


def main(args):
    vault_dir = Path(SOURCE_DIR).parent
    if not os.path.exists(vault_dir) or not os.path.exists(SOURCE_DIR):
        print(
            "Source directory not found. Process aborted.\nThe source folder should be in your vault's root directory (i.e. must not be nested)."
        )
        return

    if args.cleanup:
        remove_stale_files(POST_DEST, SOURCE_DIR)
    else:
        build_posts(
            vault_dir,
            POST_DEST,
            IMG_DEST,
            IMG_LINK,
            SOURCE_DIR,
            args.layout,
            MATH_RENDERING_MODE,
        )
        if args.update:
            remove_stale_files(POST_DEST, SOURCE_DIR)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Obsidian notes to Jekyll")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-c",
        "--cleanup",
        action="store_true",
        help="Cleans up stale posts (cannot be used with --update).",
    )
    group.add_argument(
        "-u",
        "--update",
        action="store_true",
        help="Updates the posts and cleans up stale posts (cannot be used with --cleanup).",
    )
    parser.add_argument(
        "--layout", default="post", help="Changes posts' Jekyll layout."
    )
    args = parser.parse_args()

    main(args)
