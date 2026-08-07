import re
from pathlib import Path

from src.config import POST_FOLDER, PREVENT_DOUBLE_BASEURL
from src.patterns import ANCHOR_PATTERN, LINK_PATTERN, PLACEHOLDER_PATTERN
from src.utils import slugify


def process_wikilinks(post, files):
    post.content = re.sub(
        ANCHOR_PATTERN, _anchor_replacer, post.content, flags=re.MULTILINE
    )
    post.content = re.sub(
        LINK_PATTERN,
        lambda m: _link_replacer(m, files, POST_FOLDER, PREVENT_DOUBLE_BASEURL),
        post.content,
    )
    return post


def _anchor_replacer(match):
    preceding_char = match.group(1)
    anchor = match.group("anchor").strip()
    if preceding_char == " ":
        return f"\n{{: #secid{anchor}}}"
    else:
        return f"{{: #secid{anchor}}}"


def _link_replacer(match, valid_files, post_folder, prevent_double_baseurl):
    base_url = not prevent_double_baseurl
    target = match.group("wikilink") or match.group("mdlink")
    target = target.strip()
    display = match.group("wiki_display") or match.group("md_display") or target
    display = display.strip("#")

    # skip shielding placeholders
    if re.match(PLACEHOLDER_PATTERN, target) and match.group("mdlink"):
        return f"[{display}]({target})"

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

    filename = Path(filename).stem

    if filename not in valid_files:
        print(
            f"  |  Warning: Link target not found: '{filename}'. Converted to plain text."
        )
        return f"{display}"

    dest = valid_files[filename]["dest_path"].name

    if base_url:
        return f"[{display}]({{{{ site.baseurl }}}}{{% link {post_folder / dest} %}}{anchor_suffix})"
    else:
        return f"[{display}]({{% link {post_folder / dest} %}}{anchor_suffix})"
