import re
import shutil
import frontmatter
from utils import slugify, get_dest_filepath
from config import PREVENT_DOUBLE_BASEURL


def process_single_post(
    post, source_dir, img_map, img_dest, img_url_prefix, layout, math_mode
):
    post, code_blocks = shield_content(post, mode="code")
    post, url_blocks = shield_content(post, mode="url")
    post, math_blocks = shield_content(post, mode="math")

    post = process_h1(post, layout)
    post = strip_comments(post)
    post = process_images(post, img_map, img_dest, img_url_prefix)
    post = process_wikilinks(post, source_dir)
    post = process_callouts(post)

    post = unshield(post, math_blocks)
    post = process_math(post, math_mode)
    post = fix_math_id(post)

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


def process_wikilinks(post, source_dir):
    pattern = r"(?<!\!)\[\[([^|\]]+)(?:\|([^\]]+))?\]\]"
    anchor_pattern = r"(^|\s)\^([a-zA-Z0-9-]+)(?=\s|$)"

    def _anchor_replacer(match):
        preceding_char = match.group(1)
        anchor = match.group(2).strip()
        if preceding_char == " ":
            return f"\n{{: #secid{anchor}}}"
        else:
            return f"{{: #secid{anchor}}}"

    def _link_replacer(match):
        target = match.group(1).strip()
        display = match.group(2).strip() if match.group(2) else target

        filename = target
        anchor_suffix = ""

        if "#^" in target:
            parts = target.split("#^", 1)
            filename = parts[0]
            anchor_suffix = "#secid" + parts[1].strip()
        elif "#" in target:
            parts = target.split("#", 1)
            filename = parts[0]
            anchor_suffix = "#" + slugify(parts[1])

        filename = filename.strip()

        if not filename:
            return f"[{display}]({anchor_suffix})"

        path = source_dir / (filename + ".md")
        if not path.exists():
            print(f"Warning: Wikilink target not found: '{filename}'")
            return [{display}](filename)

        post = frontmatter.load(path)
        dest_filename = get_dest_filepath(post, path)

        if PREVENT_DOUBLE_BASEURL:
            return f"[{display}]({{% link _posts/{dest_filename} %}}{anchor_suffix})"
        else:
            return f"[{display}]({{{{ site.baseurl }}}}{{% link _posts/{dest_filename} %}}{anchor_suffix})"

    post.content = re.sub(
        anchor_pattern, _anchor_replacer, post.content, flags=re.MULTILINE
    )
    post.content = re.sub(pattern, _link_replacer, post.content)
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


def fix_math_id(post):

    pattern = r"\$\$[\s\n]+({: #secid.+})"
    post.content = re.sub(pattern, r"$$\n\1", post.content)

    return post
