import re
import sys
from pathlib import Path

import frontmatter

from src.config import (
    IMG_DIR,
    IMG_FOLDER,
    MATH_RENDERING_MODE,
    POST_FOLDER,
    PREVENT_DOUBLE_BASEURL,
    VAULT_DIR,
)
from src.fs_ops import copy_images
from src.patterns import IMG_EXT
from src.process_callouts import process_callouts
from src.process_images import process_embedded_images
from src.process_links import process_wikilinks
from src.process_math import process_math
from src.text_cleanup import text_cleanup
from src.utils import shield_content, unshield


def process_posts(files, dry, layout, force, only=None):
    if only:
        stem = Path(only).stem
        if stem not in files:
            print(f"Error: Cannot find '{only}' (share: true needed).")
            sys.exit(1)
    skipped = 0
    for src, dest, post in sorted(_iter_files(files, only)):
        try:
            reason = _should_proceed(src, dest, force)

            if reason:
                print(f"{reason}: {Path(src.parent.name) / src.name} -> {dest.name}")

                if not dry:
                    post, code_blocks = shield_content(post, mode="code")
                    post, url_blocks = shield_content(post, mode="url")
                    post, math_blocks = shield_content(post, mode="math")

                    post = text_cleanup(post, layout)
                    img_map = _build_img_map(VAULT_DIR)
                    copy_images(post, img_map, IMG_DIR)
                    post = process_embedded_images(post, img_map, IMG_FOLDER)
                    post = process_wikilinks(
                        post, files, POST_FOLDER, PREVENT_DOUBLE_BASEURL
                    )
                    post = process_callouts(post)

                    post = unshield(
                        post, math_blocks, lambda x: re.sub(r"\|", r" \\vert ", x)
                    )
                    post = process_math(post, MATH_RENDERING_MODE)

                    post = unshield(post, url_blocks)
                    post = unshield(post, code_blocks)
                    frontmatter.dump(post, dest)
            else:
                skipped += 1

        except FileNotFoundError as e:
            print(f"Skipped {src.name}: {e}")
            continue

    print(f"\nProcessing finished. Skipped {skipped} unchanged files.")


def _should_proceed(src, dest, force):
    if force:
        return "Force Updating"

    if not dest.exists():
        return "Creating"

    if src.stat().st_mtime > dest.stat().st_mtime:
        return "Updating"

    return False


def _iter_files(files, only_file=None):
    if only_file:
        filename = Path(only_file).stem
        src = files[filename]["source_path"]
        dest = files[filename]["dest_path"]
        post = frontmatter.load(src)
        yield src, dest, post

    else:
        for data in files.values():
            src = data["source_path"]
            dest = data["dest_path"]
            post = frontmatter.load(src)
            yield src, dest, post


def _build_img_map(dir):
    img_map = {}
    for p in sorted(dir.rglob("*")):
        if p.is_file() and p.suffix.lower() in IMG_EXT:
            key = p.name.lower()
            if key in img_map:
                print(
                    f"Warning: Duplicate image name '{p.name}'. "
                    f"Using {img_map[key]}, ignoring {p}"
                )
                continue
            img_map[key] = p
    return img_map
