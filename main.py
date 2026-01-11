import os
import argparse
from config import *
from processor import build_posts
from cleanup import remove_stale_files


def main(args):
    post_dir = os.path.join(VAULT_DIR, POST_FOLDER)
    if args.cleanup:
        remove_stale_files(POST_DIST, post_dir)
    else:
        build_posts(
            VAULT_DIR,
            POST_DIST,
            IMG_DIST,
            IMG_LINK,
            post_dir,
            args.layout,
            MATH_RENDERING_MODE,
        )
        if args.update:
            remove_stale_files(POST_DIST, post_dir)


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
