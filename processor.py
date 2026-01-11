import os
import re
from utils import parse_md_file, get_dist_filepath, write_to_file
from transformers import (
    process_h1,
    process_images,
    process_wikilinks,
    process_math,
    strip_comments,
)


def build_posts(vault_dir, post_dist, img_dist, img_link, post_dir, layout, math_mode):
    print(f"Start processing posts in folder [ {post_dir} ]...\n")
    setup_dir(post_dist, img_dist)
    img_map = build_file_map(vault_dir)

    for root, _, files in os.walk(post_dir):
        for filename in files:
            if filename.endswith(".md"):
                source_path, frontmatter, body = parse_md_file(root, filename)
                _, new_filepath = get_dist_filepath(
                    root, filename, frontmatter, post_dist
                )
                if should_proceed(source_path, new_filepath):
                    print(f"Processing: {filename} -> {new_filepath}")
                    body, code_blocks = create_code_shield(body)

                    body, frontmatter = process_h1(body, frontmatter, layout)
                    body = strip_comments(body)
                    body = process_images(body, img_map, img_dist, img_link)
                    body = process_wikilinks(body)
                    body, frontmatter = process_math(body, frontmatter, math_mode)

                    body = unshield(body, code_blocks)
                    write_to_file(new_filepath, frontmatter, body)
                else:
                    print(f"Skipping (Unchanged): {filename}")

            else:
                print(f"Skipping (Not an md file): {filename}")
    print("\nProcessing finished.")


def build_file_map(directory):
    img_txt = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp")
    file_map = {}
    for root, _, files in os.walk(directory):
        for f in files:
            if f.lower().endswith(img_txt):
                file_map[f.lower()] = os.path.join(root, f)
    return file_map


def setup_dir(post_dist, img_dist):
    if not os.path.exists(post_dist):
        os.makedirs(post_dist, exist_ok=True)
        print(f"destination post folder not found, creating {post_dist}...")
    if not os.path.exists(img_dist):
        os.makedirs(img_dist, exist_ok=True)
        print(f"destination image folder not found, creating {img_dist}...")


def should_proceed(source_path, dest_path):
    if not os.path.exists(dest_path):
        return True

    return os.path.getmtime(source_path) > os.path.getmtime(dest_path)


def create_code_shield(body):

    def shield_replacer(match):
        placeholder = f"&&CODE_BLOCK_{len(code_blocks)}&&"
        code_blocks.append(match.group(0))
        return placeholder

    code_blocks = []
    code_pattern = r"(```.*?```|`.*?`)"
    code_shield = re.sub(code_pattern, shield_replacer, body, flags=re.DOTALL)

    return code_shield, code_blocks


def unshield(code_shield, code_blocks):
    for i, original_code in enumerate(code_blocks):
        code_shield = code_shield.replace(f"&&CODE_BLOCK_{i}&&", original_code)
    unshield_content = code_shield

    return unshield_content
