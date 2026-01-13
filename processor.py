import re
import frontmatter
from pathlib import Path
from templates import CALLOUT_CSS
from utils import get_dest_filepath
from transformers import (
    process_h1,
    process_images,
    process_wikilinks,
    process_math,
    process_callouts,
    strip_comments,
)


def build_posts(
    post_dest, img_dest, img_url_prefix, post_dir, includes_dir, layout, math_mode, dry
):
    if dry:
        print("------------ DRY RUN MODE -------------")
        print("Operations will be printed but files won't be changed.\n")

    print(f"Start processing posts in folder [ {post_dir} ]...")
    print(f"Destination path: [ {post_dest} ]\n")
    img_map = build_img_map(post_dir.parent)

    if not dry:
        setup_dir(post_dest, img_dest)
        ensure_css_exists(includes_dir, css_name="obsidian-callouts.html")

    for source_path in post_dir.rglob("*.md"):
        post = frontmatter.load(source_path)
        dest_path = get_dest_filepath(source_path, post_dest, post)
        filename = source_path.name
        new_fname = dest_path.name
        if should_proceed(source_path, dest_path):
            print(f"Processing: {filename} -> {new_fname}")
            if not dry:
                post, code_blocks = create_code_shield(post)

                post = process_h1(post, layout)
                post = strip_comments(post)
                post = process_images(post, img_map, img_dest, img_url_prefix)
                post = process_wikilinks(post)
                post = process_math(post, math_mode)
                post = process_callouts(post)

                post = unshield(post, code_blocks)
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


def setup_dir(post_dest, img_dest):
    for path in [post_dest, img_dest]:
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            print(f"Destination folder not found, creating {path}...")


def should_proceed(source_path, dest_path):
    if not dest_path.exists():
        return True

    return source_path.stat().st_mtime > dest_path.stat().st_mtime


def create_code_shield(post):

    def shield_replacer(match):
        placeholder = f"&&CODE_BLOCK_{len(code_blocks)}&&"
        code_blocks.append(match.group(0))
        return placeholder

    code_blocks = []
    code_pattern = r"(```.*?```|`.*?`)"
    post.content = re.sub(code_pattern, shield_replacer, post.content, flags=re.DOTALL)

    return post, code_blocks


def unshield(code_shielded_post, code_blocks):
    for i, original_code in enumerate(code_blocks):
        code_shielded_post.content = code_shielded_post.content.replace(
            f"&&CODE_BLOCK_{i}&&", original_code
        )
    unshield_post = code_shielded_post

    return unshield_post


def ensure_css_exists(dir, css_name):
    css_path = dir / css_name
    if not css_path.exists():
        print(f"--> Creating default callout CSS at: {css_path}")
        css_path.parent.mkdir(parents=True, exist_ok=True)
        css_path.write_text(CALLOUT_CSS, encoding="utf-8")
