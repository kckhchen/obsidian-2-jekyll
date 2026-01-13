import re
import shutil
from pathlib import Path
from utils import slugify


def process_single_post(post, img_map, img_dest, img_url_prefix, layout, math_mode):
    post, code_blocks = shield_content(post, mode="code")
    post, url_blocks = shield_content(post, mode="url")
    post, math_blocks = shield_content(post, mode="math")

    post = process_h1(post, layout)
    post = strip_comments(post)
    post = process_images(post, img_map, img_dest, img_url_prefix)
    post = process_wikilinks(post)
    post = process_callouts(post)

    post = unshield(post, math_blocks)
    post = process_math(post, math_mode)

    post = unshield(post, url_blocks)
    post = unshield(post, code_blocks)
    return post


def process_h1(post, layout="post"):
    post["layout"] = post.get("layout") or layout
    h1_pattern = r"^\s*#\s+(.+?)$"
    h1_match = re.search(h1_pattern, post.content, flags=re.MULTILINE)

    if h1_match:
        title = h1_match.group(1).strip()
        post["title"] = post.get("title") or title
        post.content = re.sub(
            h1_pattern, "", post.content, count=1, flags=re.MULTILINE
        ).strip()
    return post


def strip_comments(post):
    comment_pattern = r"%%.*?%%"
    post.content = re.sub(comment_pattern, "", post.content, flags=re.DOTALL)
    return post


def process_images(post, img_map, img_dest, url_prefix):
    # (.*?) The filename
    # (?:\|(\d+))? Optional pipe followed by digits (Width)
    pattern = r"!\[\[([^|\]]+)(?:\|(\d+))?\]\]"

    def replacer(match):
        img_name = match.group(1).strip()
        width = match.group(2)

        if img_name.lower() in img_map:
            shutil.copy2(img_map[img_name.lower()], img_dest / img_name)
            updated_link = f"![]({url_prefix / img_name})"
            if width:
                updated_link += f'{{: width="{width}" }}'
            return updated_link

        return match.group(0)

    post.content = re.sub(pattern, replacer, post.content)
    return post


def process_wikilinks(post):
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

    post.content = re.sub(
        anchor_pattern, anchor_replacer, post.content, flags=re.MULTILINE
    )

    def link_replacer(match):
        target = match.group(1).strip()
        display = match.group(2).strip() if match.group(2) else target

        if "#^" in target:
            parts = target.split("#^", 1)
            filename = parts[0].strip()
            block_id = "secid" + parts[1].strip()

            if not filename:
                return f"[{display}](#{block_id})"

            slug = slugify(filename)
            return f"[{display}](../{slug}#{block_id})"

        elif "#" in target:
            parts = target.split("#", 1)
            filename = parts[0].strip()
            section = slugify(parts[1])

            if not filename:
                return f"[{display}](#{section})"

            slug = slugify(filename)
            return f"[{display}](../{slug}#{section})"

        slug = slugify(target)
        return f"[{display}](../{slug})"

    post.content = re.sub(pattern, link_replacer, post.content)
    return post


def needs_math(content):
    has_block_math = bool(re.search(r"\$\$.*?\$\$", content, flags=re.DOTALL))
    has_inline_math = bool(re.search(r"(?<!\\)\$[^ \t\n\$].*?\$", content))

    return has_block_math or has_inline_math


def process_math(post, math_mode):
    if needs_math(post.content):
        mathjax_script = '<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@4/tex-mml-chtml.js"></script>'
        inline_math_pattern = r"(?<!\\|\$)\$([^$]+?)(?<!\\)\$(?!\$)"
        post.content = re.sub(inline_math_pattern, r"\\\\(\1\\\\)", post.content)
        post.content = re.sub(
            r"(\$\$.*?\$\$)", r"\n\1\n", post.content, flags=re.DOTALL
        )

        if math_mode == "inject_cdn":
            post.content += f"\n\n{mathjax_script}"
        elif math_mode == "metadata":
            post["math"] = post.get("math") or True
        else:
            print(
                'Math blocks detected but no rendering mode is selected. Please either set MATH_RENDERING_MODE = "inject_cdn" or "metadata".\n'
            )
    return post


def needs_callout(content, callout_pattern):
    return bool(re.search(callout_pattern, content))


def process_callouts(post):

    def _replacer(match):
        callout_type = match.group(1).lower()
        collapse = match.group(2)
        title = match.group(3).strip()
        body = re.sub(r"^>\s?", "", match.group(4), flags=re.MULTILINE)
        return render_callout(callout_type, title, body, collapse)

    callout_pattern = re.compile(
        r"^> \[!\s*(\w+)\]([+\-]?)(.*?)\n((?:^>.*\n?)*)", re.MULTILINE
    )

    if needs_callout(post.content, callout_pattern):
        post.content = callout_pattern.sub(_replacer, post.content)
        post.content += "\n\n{% include obsidian-callouts.html %}"

    return post


def render_callout(callout_type, title, body, collapse):
    title = title or callout_type.capitalize()
    tag_map = {"+": "details open", "-": "details"}
    open_tag = tag_map.get(collapse)
    if open_tag:
        content = f"""<{open_tag}>
    <summary class="callout-title">{title}</summary>
    {body}
</details>"""
    else:
        content = f"""<div class="callout-title">{title}</div>
{body}"""

    return (
        f'<div class="callout callout-{callout_type}" markdown="1">\n{content}\n</div>'
    )


def shield_content(post, mode):

    def _replacer(match):
        key = f"&&{mode.upper()}_{len(stash)}&&"
        stash[key] = match.group(0)
        return key

    if mode == "code":
        pattern = r"(```[\s\S]*?```|`[^`\n]+`)"
    elif mode == "math":
        pattern = r"(\$\$[\s\S]*?\$\$|(?<!\$)\$[^$]+\$(?!\$))"
    elif mode == "url":
        pattern = r"https?://[^)\s]+"
    else:
        raise ValueError(f"Unknown shield type: {mode}")

    stash = {}
    post.content = re.sub(pattern, _replacer, post.content)
    return post, stash


def unshield(post, stash):
    for key, original_text in stash.items():
        post.content = post.content.replace(key, original_text)
    return post
