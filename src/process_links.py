import re
import frontmatter
from pathlib import Path

from . import settings
from .utils import slugify, get_dest_fpath


def process_wikilinks(post, source_dir):
    pattern = r"(?<!\!)\[\[([^|\]]+)(?:\|([^\]]+))?\]\]"
    anchor_pattern = r"(^|\s)\^([a-zA-Z0-9-]+)(?=\s|$)"
    post_folder = Path(settings.config.POST_FOLDER)

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
        dest_filename = get_dest_fpath(post, path)

        if settings.config.PREVENT_DOUBLE_BASEURL:
            return f"[{display}]({{% link {post_folder / dest_filename} %}}{anchor_suffix})"
        else:
            return f"[{display}]({{{{ site.baseurl }}}}{{% link {post_folder / dest_filename} %}}{anchor_suffix})"

    post.content = re.sub(
        anchor_pattern, _anchor_replacer, post.content, flags=re.MULTILINE
    )
    post.content = re.sub(pattern, _link_replacer, post.content)
    return post
