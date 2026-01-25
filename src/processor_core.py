import re
import frontmatter
from pathlib import Path

from .utils import shield_content, unshield
from .fs_ops import announce_paths, setup_dir, ensure_css_exists, build_img_map
from .text_cleanup import process_h1, strip_comments
from .process_math import process_math
from .process_images import process_embedded_images
from .process_links import process_wikilinks
from .process_callouts import process_callouts


def pre_process(vault_dir, post_dir, img_dir, dry):
    announce_paths(vault_dir, post_dir, dry)
    setup_dir(post_dir, img_dir, dry)
    ensure_css_exists("obsidian-callouts.html", dry)
    img_map = build_img_map(vault_dir)
    return img_map


def process_posts(valid_files, img_map, img_dir, dry, layout, force, only=None):
    try:
        skipped = 0
        for src, dest, post in sorted(_iter_files(valid_files, only)):

            if not _should_proceed(src, dest, force):
                skipped += 1
                continue

            print(f"Processing: {Path(src.parent.name) / src.name} -> {dest.name}")

            if not dry:
                post = _process_single_post(post, valid_files, img_map, img_dir, layout)
                frontmatter.dump(post, dest)

    except (ValueError, FileNotFoundError) as e:
        print(e)
        return

    print(f"\nProcessing finished. Skipped {skipped} unchanged files.")


def _should_proceed(src, dest, force):
    if not dest.exists() or force:
        return True

    return src.stat().st_mtime > dest.stat().st_mtime


def _process_single_post(post, valid_files, img_map, img_dir, layout):
    post, code_blocks = shield_content(post, mode="code")
    post, url_blocks = shield_content(post, mode="url")
    post, math_blocks = shield_content(post, mode="math")

    post = process_h1(post, layout)
    post = strip_comments(post)
    post = process_embedded_images(post, img_map, img_dir)
    post = process_wikilinks(post, valid_files)
    post = process_callouts(post)

    post = unshield(post, math_blocks, lambda x: re.sub(r"\|", r" \\vert ", x))
    post = process_math(post)

    post = unshield(post, url_blocks)
    post = unshield(post, code_blocks)
    return post


def _iter_files(files, only_file=None):

    if only_file:
        filename = Path(only_file).stem

        if filename not in files:
            raise ValueError(f"Error: Cannot find '{only_file}' (share: true needed).")

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
