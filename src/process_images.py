import re
import shutil
from pathlib import Path
from . import settings


def process_images(post, img_map, img_dir):
    pattern = r"!\[\[([^|\]]+)(?:\|(\d+))?\]\]"
    img_folder = Path(settings.config.IMG_FOLDER)

    def _replacer(match):
        img_name = match.group(1).strip()
        width = match.group(2)

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
            return match.group(0)

    post.content = re.sub(pattern, _replacer, post.content)
    return post
