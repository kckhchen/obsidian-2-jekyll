import re
from pathlib import Path

from . import settings
from .utils import slugify


def process_wikilinks(post, valid_files):
    pattern = r"(?<!\!)\[\[(?P<wikilink>[^|\]]+)(?:\|(?P<wiki_display>[^\]]+))?\]\]|(?<!\!)\[(?P<md_display>[^\]]*)\]\((?P<mdlink>[^\)]+)\)"
    anchor_pattern = r"(^|\s)\^(?P<anchor>[a-zA-Z0-9-]+)(?=\s|$)"

    post.content = re.sub(
        anchor_pattern, _anchor_replacer, post.content, flags=re.MULTILINE
    )
    post.content = re.sub(
        pattern, lambda m: _link_replacer(m, valid_files), post.content
    )
    return post


def _anchor_replacer(match):
    preceding_char = match.group(1)
    anchor = match.group("anchor").strip()
    if preceding_char == " ":
        return f"\n{{: #secid{anchor}}}"
    else:
        return f"{{: #secid{anchor}}}"


def _link_replacer(match, valid_files):
    post_folder = Path(settings.config.POST_FOLDER)

    target = match.group("wikilink") or match.group("mdlink")
    target = target.strip()
    display = match.group("wiki_display") or match.group("md_display") or target

    # skip shielding placeholders
    if re.match(r"^&&\w+_\d+&&$", target) and match.group("mdlink"):
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

    if not filename in valid_files:
        print(f"  |  Warning: Link target not found: '{filename}'")
        return f"[{display}]({filename})"

    dest = valid_files[filename]["dest_path"].name

    if settings.config.PREVENT_DOUBLE_BASEURL:
        return f"[{display}]({{% link {post_folder / dest} %}}{anchor_suffix})"
    else:
        return f"[{display}]({{{{ site.baseurl }}}}{{% link {post_folder / dest} %}}{anchor_suffix})"
