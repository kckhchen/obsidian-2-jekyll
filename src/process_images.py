import re
import shutil
from pathlib import Path

from . import settings
from .patterns import IMG_EXT


def process_embedded_images(post, img_map, img_dir):
    pattern = (
        r"!\[\[(?P<wikilink>[^|\]]+?)(?:\\?\|(?P<wiki_opt>[^\]]*))?\]\]"
        r"|!\[(?P<md_opt>[^\]]*)\]\((?P<mdlink>[^)]+)\)"
    )

    post.content = re.sub(
        pattern, lambda m: _embedded_image_replacer(m, img_map, img_dir), post.content
    )
    return post


def _split_opt(raw, is_md):
    raw = (raw or "").strip()

    if is_md and "|" in raw:
        alt, _, size = raw.rpartition("|")
    elif raw and raw.replace("x", "", 1).isdigit():
        alt, size = "", raw
    else:
        alt, size = raw, ""

    w, _, h = size.partition("x")
    return alt.strip(), (w if w.isdigit() else ""), (h if h.isdigit() else "")


def _embedded_image_replacer(match, img_map, img_dir):
    img_folder = Path(settings.config.IMG_FOLDER)

    is_md = match.group("mdlink") is not None
    img_name = (match.group("mdlink") if is_md else match.group("wikilink")).strip()
    alt, width, height = _split_opt(
        match.group("md_opt") if is_md else match.group("wiki_opt"), is_md
    )

    if Path(img_name).suffix.lower() not in IMG_EXT:
        return f"![{alt}]({img_name})"

    if img_name.lower() in img_map:
        shutil.copy2(img_map[img_name.lower()], img_dir / img_name)
        updated_link = (
            f"![{alt}]({{{{ site.baseurl }}}}{{% link {img_folder / img_name} %}})"
        )

        attrs = [f'{k}="{v}"' for k, v in (("width", width), ("height", height)) if v]
        if attrs:
            updated_link += "{: " + " ".join(attrs) + " }"

        return updated_link
    else:
        print(
            f"  |  Warning: Image target not found in Vault: {img_name}. Link kept as-is."
        )
        return match.group(0)
