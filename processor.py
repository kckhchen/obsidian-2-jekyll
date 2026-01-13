import re
import frontmatter
from pathlib import Path
from templates import CALLOUT_CSS
from utils import get_dest_filepath
from transformers import process_single_post


def process_posts(
    post_dest, img_dest, img_url_prefix, post_dir, includes_dir, layout, math_mode, dry
):
    announce_paths(post_dir, post_dest, dry)
    setup_dir(post_dest, img_dest, dry)
    ensure_css_exists(includes_dir, css_name="obsidian-callouts.html", dry=dry)
    img_map = build_img_map(post_dir.parent)

    for source_path in post_dir.rglob("*.md"):
        post = frontmatter.load(source_path)
        dest_path = get_dest_filepath(source_path, post_dest, post)
        filename, new_fname = source_path.name, dest_path.name
        if should_proceed(source_path, dest_path):
            print(f"Processing: {filename} -> {new_fname}")
            if not dry:
                post = process_single_post(
                    post, img_map, img_dest, img_url_prefix, layout, math_mode
                )
                frontmatter.dump(post, dest_path)
        else:
            print(f"Skipping (Unchanged): {filename}")
    print("\nProcessing finished.")


def build_img_map(dir):
    extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}
    img_map = {}
    for p in dir.rglob("*"):
        if p.is_file() and p.suffix.lower() in extensions:
            img_map[p.name.lower()] = p

    return img_map


def setup_dir(post_dest, img_dest, dry):
    for path in [post_dest, img_dest]:
        if not path.exists():
            print(f"Destination folder not found, creating {path}...")
            if not dry:
                path.mkdir(parents=True, exist_ok=True)


def should_proceed(source_path, dest_path):
    if not dest_path.exists():
        return True

    return source_path.stat().st_mtime > dest_path.stat().st_mtime


def ensure_css_exists(dir, css_name, dry):
    css_path = dir / css_name
    if not css_path.exists():
        print(f"--> Creating default callout CSS at: {css_path}")
        if not dry:
            css_path.parent.mkdir(parents=True, exist_ok=True)
            css_path.write_text(CALLOUT_CSS, encoding="utf-8")


def announce_paths(post_dir, post_dest, dry):
    if dry:
        print("------------ DRY RUN MODE -------------")
        print("Operations will be printed but files won't be changed.\n")

    print(f"Start processing posts in folder [ {post_dir} ]...")
    print(f"Destination path: [ {post_dest} ]\n")
