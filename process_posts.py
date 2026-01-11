import os
import re
import shutil
from datetime import datetime
from env import *

POST_DIR = os.path.join(VAULT_DIR, POST_FOLDER)
IMG_DIR = os.path.join(VAULT_DIR, IMG_FOLDER)


def build_file_map(directory):
    file_map = {}
    for root, _, files in os.walk(directory):
        for f in files:
            file_map[f.lower()] = os.path.join(root, f)
    return file_map


def setup_dir(post_dist, img_dist):
    if os.path.exists(post_dist):
        shutil.rmtree(post_dist)
    if os.path.exists(img_dist):
        shutil.rmtree(img_dist)
    os.makedirs(post_dist, exist_ok=True)
    os.makedirs(img_dist, exist_ok=True)


def parse_md_file(root, filename):
    if not filename.endswith(".md"):
        return None, None
    content = open(os.path.join(root, filename), "r", encoding="utf-8").read()
    fm_match = re.search(r"^---\n(.*?)\n---\n", content, flags=re.DOTALL)
    if not fm_match:
        return "", content
    return fm_match.group(1), content[fm_match.end() :]


def update_filename(root, filename, frontmatter):
    stat_info = os.stat(os.path.join(root, filename))
    creation_date = datetime.fromtimestamp(stat_info.st_birthtime).strftime("%Y-%m-%d")
    date_match = re.search(r"date:\s*(\d{4}-\d{2}-\d{2})", frontmatter)
    date_str = date_match.group(1) if date_match else creation_date
    clean_name = re.sub(r"\d{4}-\d{2}-\d{2}-", "", filename).replace(" ", "-").lower()
    new_name = f"{date_str}-{clean_name}"
    return new_name


def process_h1(body, frontmatter):
    frontmatter = f"layout: post\n{frontmatter}"
    h1_pattern = r"^\s*#\s+(.+?)$"
    h1_match = re.search(h1_pattern, body, flags=re.MULTILINE)

    if h1_match:
        if "title:" not in frontmatter:
            title = h1_match.group(1).strip()
            frontmatter = f"title: {title}\n{frontmatter}"
        body = re.sub(h1_pattern, "", body, count=1, flags=re.MULTILINE).strip()
    return body, frontmatter


def process_images(body, img_map, img_dist):
    # 1. (.*?) -> The filename
    # 2. (?:\|(\d+))? -> Optional pipe followed by digits (Width)
    # 3. (?:\|(.*?))? -> Optional pipe followed by text (Alt/Alias)
    pattern = r"!\[\[([^|\]]+)(?:\|(\d+))?(?:\|([^\]]+))?\]\]"

    def replacer(match):
        img_name = match.group(1).strip()
        width = match.group(2)

        if img_name.lower() in img_map:
            shutil.copy2(img_map[img_name.lower()], os.path.join(IMG_DIST, img_name))
            updated_link = f"![]({os.path.join(img_dist, img_name)})"
            if width:
                updated_link += f'{{: width="{width}" }}'
            return updated_link

        return match.group(0)

    return re.sub(pattern, replacer, body)


def process_wikilinks(body):
    # Group 1: Target, Group 2: |Display (optional)
    pattern = r"(?<!\!)\[\[([^|\]]+)(?:\|([^\]]+))?\]\]"

    def link_replacer(match):
        target = match.group(1).strip()
        display = match.group(2).strip() if match.group(2) else target
        slug = target.replace(" ", "-").lower()
        return f"[{display}](../{slug}/)"

    body = re.sub(pattern, link_replacer, body)
    return body


def needs_mathjax(body):
    clean_body = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    clean_body = re.sub(r"`.*?`", "", clean_body)
    has_block_math = bool(re.search(r"\$\$.*?\$\$", clean_body, flags=re.DOTALL))
    has_inline_math = bool(re.search(r"(?<!\\)\$[^ \t\n\$].*?\$", clean_body))

    return has_block_math or has_inline_math


def process_math(body):

    def shield_replacer(match):
        placeholder = f"%%CODE_BLOCK_PLACEHOLDER_{len(code_blocks)}%%"
        code_blocks.append(match.group(0))
        return placeholder

    def math_block_replacer(match):
        inner_math = match.group(1)
        # change \\ to \\\\\\\\ so that MD will show \\\\ and html will read \\
        # which is important for math block line break
        fixed_math = inner_math.replace(r"\\", r"\\\\\\\\")
        # if math block starts with \begin{...} return the raw math block
        # (i.e. strip away $$...$$ since \begin{} is a math block itself)
        # else simply swap $$...$$ for \[...\] and apply pretty line breaks
        if re.match(r"^\s*\\begin\{.+?\}", fixed_math.strip()):
            return fixed_math
        else:
            return f"\n\\\[{fixed_math}\\\]\n"

    if needs_mathjax(body):
        code_blocks = []
        code_shield = re.sub(
            r"(```.*?```|`.*?`)", shield_replacer, body, flags=re.DOTALL
        )

        # look for math block and apply changes first
        code_shield = re.sub(
            r"\$\$(.*?)\$\$", math_block_replacer, code_shield, flags=re.DOTALL
        )
        # replace $...$ to \(...\)
        code_shield = re.sub(
            r"(?<!\\)\$([^$]+?)(?<!\\)\$", r"\\\\(\1\\\\)", code_shield
        )
        # add this line at the end for html to recognize
        code_shield += "\n\n{% include mathjax.html %}"

        for i, original_code in enumerate(code_blocks):
            code_shield = code_shield.replace(
                f"%%CODE_BLOCK_PLACEHOLDER_{i}%%", original_code
            )

        return code_shield
    return body


def write_to_file(post_dist, new_filename, frontmatter, body):
    with open(os.path.join(post_dist, new_filename), "w", encoding="utf-8") as f:
        f.write(f"---\n{frontmatter.strip()}\n---\n\n{body.strip()}")
    print(f"Done: {new_filename}")


# --- Main Logic ---


def process_post():
    setup_dir(POST_DIST, IMG_DIST)
    img_map = build_file_map(IMG_DIR)

    for root, _, files in os.walk(POST_DIR):
        for filename in files:
            frontmatter, body = parse_md_file(root, filename)

            if not frontmatter is None:
                new_filename = update_filename(root, filename, frontmatter)
                body, frontmatter = process_h1(body, frontmatter)
                body = process_images(body, img_map, IMG_DIST)
                body = process_wikilinks(body)
                body = process_math(body)

                write_to_file(POST_DIST, new_filename, frontmatter, body)


if __name__ == "__main__":
    process_post()
