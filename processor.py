import os
import re
import frontmatter

from utils import parse_md_file, get_dest_filepath
from transformers import (
    process_h1,
    process_images,
    process_wikilinks,
    process_math,
    strip_comments,
)


def build_posts(
    vault_dir, post_dest, img_dest, img_link, post_dir, layout, math_mode, dry
):
    print(f"Start processing posts in folder [ {post_dir} ]...")
    print(f"Destination path: [ {post_dest} ]\n")
    if not dry:
        setup_dir(post_dest, img_dest)
    img_map = build_file_map(vault_dir)

    for root, _, files in os.walk(post_dir):
        for filename in files:
            if filename.endswith(".md"):
                source_path, post = parse_md_file(root, filename)
                new_name, dest_path = get_dest_filepath(
                    source_path, filename, post, post_dest
                )
                if should_proceed(source_path, dest_path):
                    print(f"Processing: {filename} -> {new_name}")
                    if not dry:
                        post, code_blocks = create_code_shield(post)

                        post = process_h1(post, layout)
                        post = strip_comments(post)
                        post = process_images(post, img_map, img_dest, img_link)
                        post = process_wikilinks(post)
                        post = process_math(post, math_mode)

                        post = unshield(post, code_blocks)
                        frontmatter.dump(post, dest_path)
                else:
                    print(f"Skipping (Unchanged): {filename}")

            else:
                print(f"Skipping (Not md file): {filename}")
    print("\nProcessing finished.")


def build_file_map(directory):
    img_txt = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp")
    file_map = {}
    for root, _, files in os.walk(directory):
        for f in files:
            if f.lower().endswith(img_txt):
                file_map[f.lower()] = os.path.join(root, f)
    return file_map


def setup_dir(post_dest, img_dest):
    if not os.path.exists(post_dest):
        os.makedirs(post_dest, exist_ok=True)
        print(f"destination post folder not found, creating {post_dest}...")
    if not os.path.exists(img_dest):
        os.makedirs(img_dest, exist_ok=True)
        print(f"destination image folder not found, creating {img_dest}...")


def should_proceed(source_path, dest_path):
    if not os.path.exists(dest_path):
        return True

    return os.path.getmtime(source_path) > os.path.getmtime(dest_path)


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
