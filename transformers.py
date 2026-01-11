import os
import re
import shutil


def process_h1(body, frontmatter, layout="post"):
    frontmatter = f"layout: {layout}\n{frontmatter}"
    h1_pattern = r"^\s*#\s+(.+?)$"
    h1_match = re.search(h1_pattern, body, flags=re.MULTILINE)

    if h1_match:
        if "title:" not in frontmatter:
            title = h1_match.group(1).strip()
            frontmatter = f"title: {title}\n{frontmatter}"
        body = re.sub(h1_pattern, "", body, count=1, flags=re.MULTILINE).strip()
    return body, frontmatter


def strip_comments(body):
    comment_pattern = r"%%.*?%%"
    body = re.sub(comment_pattern, "", body, flags=re.DOTALL)
    return body


def process_images(body, img_map, img_dist, img_link):
    # (.*?) The filename
    # (?:\|(\d+))? Optional pipe followed by digits (Width)
    # (?:\|(.*?))? Optional pipe followed by text (Alt/Alias)
    pattern = r"!\[\[([^|\]]+)(?:\|(\d+))?(?:\|([^\]]+))?\]\]"

    def replacer(match):
        img_name = match.group(1).strip()
        width = match.group(2)

        if img_name.lower() in img_map:
            shutil.copy2(img_map[img_name.lower()], os.path.join(img_dist, img_name))
            updated_link = f"![]({os.path.join(img_link, img_name)})"
            if width:
                updated_link += f'{{: width="{width}" }}'
            return updated_link

        return match.group(0)

    return re.sub(pattern, replacer, body)


def process_wikilinks(body):
    # Group 1: Target, Group 2: |Display (optional)
    pattern = r"(?<!\!)\[\[([^|\]]+)(?:\|([^\]]+))?\]\]"
    # Look for "\n" or " " followed by the anchor "^hash" and ending with " " or end-of-file
    anchor_pattern = r"(^|\s)\^([a-zA-Z0-9-]+)(?=\s|$)"

    def anchor_replacer(match):
        preceding_char = match.group(1)
        anchor = match.group(2).strip()
        if preceding_char == " ":
            return f"\n{{: #secid{anchor}}}"
        else:
            return f"{{: #secid{anchor}}}"

    body = re.sub(anchor_pattern, anchor_replacer, body, flags=re.MULTILINE)

    def link_replacer(match):
        target = match.group(1).strip()
        display = match.group(2).strip() if match.group(2) else target

        if "#^" in target:
            parts = target.split("#^", 1)
            filename = parts[0].strip()
            block_id = "secid" + parts[1].strip()

            if not filename:
                return f"[{display}](#{block_id})"

            slug = filename.replace(" ", "-").lower()
            return f"[{display}](../{slug}#{block_id})"

        elif "#" in target:
            parts = target.split("#", 1)
            filename = parts[0].strip()
            section = parts[1].strip().lower().replace(" ", "-")

            if not filename:
                return f"[{display}](#{section})"

            slug = filename.replace(" ", "-").lower()
            return f"[{display}](../{slug}#{section})"

        slug = target.replace(" ", "-").lower()
        return f"[{display}](../{slug})"

    body = re.sub(pattern, link_replacer, body)
    return body


def needs_math(body):
    no_code = re.sub(r"(```.*?```|`.*?`)", "", body, flags=re.DOTALL)
    has_block_math = bool(re.search(r"\$\$.*?\$\$", no_code, flags=re.DOTALL))
    has_inline_math = bool(re.search(r"(?<!\\)\$[^ \t\n\$].*?\$", no_code))

    return has_block_math or has_inline_math


def process_math(body, frontmatter, math_mode):
    if needs_math(body):
        mathjax_script = '<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@4/tex-mml-chtml.js"></script>'
        inline_math_pattern = r"(?<!\\|\$)\$([^$]+?)(?<!\\)\$(?!\$)"
        body = re.sub(inline_math_pattern, r"\\\\(\1\\\\)", body)

        if math_mode == "inject_cdn":
            body += f"\n\n{mathjax_script}"
        elif math_mode == "metadata":
            frontmatter = f"math: true\n{frontmatter}"
        else:
            print(
                'Math blocks detected but no rendering mode is selected. Please either set MATH_RENDERING_MODE = "inject_cdn" or "metadata".\n'
            )
    return body, frontmatter
