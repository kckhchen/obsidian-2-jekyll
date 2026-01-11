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


def process_images(body, img_map, img_dist, img_link):
    # 1. (.*?) -> The filename
    # 2. (?:\|(\d+))? -> Optional pipe followed by digits (Width)
    # 3. (?:\|(.*?))? -> Optional pipe followed by text (Alt/Alias)
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
            return f"\n{fixed_math}"
        else:
            return f"\n\n\\\[{fixed_math}\\\]\n"

    if needs_mathjax(body):
        code_blocks = []
        code_shield = re.sub(
            r"(```.*?```|`.*?`)", shield_replacer, body, flags=re.DOTALL
        )

        # look for math block and apply changes first
        code_shield = re.sub(
            r"\s*\$\$(.*?)\$\$\s*", math_block_replacer, code_shield, flags=re.DOTALL
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
