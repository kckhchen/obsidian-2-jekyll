import re
import shutil
from pathlib import Path
from . import settings


def process_embedded_images(post, img_map, img_dir):
    pattern = r"!\[\[(?P<wikilink>[^|\]]+)(?:\|(?P<wiki_width>\d+)[^\]]*)?\]\]|!\[(?P<md_width>\d*)[^\]]*\]\((?P<mdlink>[^)]+)\)"

    post.content = re.sub(
        pattern, lambda m: _embedded_image_replacer(m, img_map, img_dir), post.content
    )
    return post


def _embedded_image_replacer(match, img_map, img_dir):
    img_ext = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp")
    img_folder = Path(settings.config.IMG_FOLDER)

    img_name = match.group("wikilink") or match.group("mdlink")
    img_name = img_name.strip()
    width = match.group("wiki_width") or match.group("md_width") or ""

    if Path(img_name).suffix not in img_ext:
        return f"![{width}]({img_name})"

    if img_name.lower() in img_map:
        shutil.copy2(img_map[img_name.lower()], img_dir / img_name)
        updated_link = (
            f"![]({{{{ site.baseurl }}}}{{% link {img_folder / img_name} %}})"
        )
        if width:
            updated_link += f'{{: width="{width}" }}'
        return updated_link
    else:
        print(
            f"  |  Warning: Image target not found in Vault: {img_name}. Removed image tag."
        )
        return ""
