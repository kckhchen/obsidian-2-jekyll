import re
import shutil
from pathlib import Path
from . import settings


def process_embedded_images(post, img_map, img_dir):
    img_ext = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp")
    pattern = r"!\[\[(?P<wikilink>[^|\]]+)(?:\|(?P<wiki_width>\d+)[^\]]*)?\]\]|!\[(?P<md_width>\d*)[^\]]*\]\((?P<mdlink>[^)]+)\)"
    img_folder = Path(settings.config.IMG_FOLDER)

    def _replacer(match):
        img_name = match.group("wikilink") or match.group("mdlink")
        img_name = img_name.strip()
        width = match.group("wiki_width") or match.group("md_width") or ""

        if Path(img_name).suffix not in img_ext:
            print(f"Skipping {img_name}: not an image.")
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
            print(f"Image target not found in Vault: {img_name}")
            return f"![{width}]({img_name})"

    post.content = re.sub(pattern, _replacer, post.content)
    return post
