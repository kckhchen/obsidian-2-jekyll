from pathlib import Path
import shutil
import re

from src.callout_styles import CALLOUT_CSS
from src.config import INCLUDES_FOLDER, JEKYLL_DIR
from src.patterns import IMG_EXT, IMG_PATTERN


def build_img_map(dir):
    img_map = {}
    for p in sorted(dir.rglob("*")):
        if p.is_file() and p.suffix.lower() in IMG_EXT:
            key = p.name.lower()
            if key in img_map:
                print(
                    f"Warning: Duplicate image name '{p.name}'. "
                    f"Using {img_map[key]}, ignoring {p}"
                )
                continue
            img_map[key] = p
    return img_map


def setup_dir(post_dir, img_dir, dry):
    for path in [post_dir, img_dir]:
        if not path.exists():
            print(f"---- Destination folder not found, creating {path} ----")
            if not dry:
                path.mkdir(parents=True, exist_ok=True)


def ensure_css_exists(css_name, dry):
    includes_dir = Path(JEKYLL_DIR) / INCLUDES_FOLDER
    css_path = includes_dir / css_name
    if not css_path.exists():
        print(f"---- Creating default callout CSS at: {css_path} ----")
        if not dry:
            css_path.parent.mkdir(parents=True, exist_ok=True)
            css_path.write_text(CALLOUT_CSS, encoding="utf-8")


def copy_images(post, img_map, img_dir):
    for match in re.finditer(IMG_PATTERN, post.content):
        is_md = match.group("mdlink") is not None
        img_name = (match.group("mdlink") if is_md else match.group("wikilink")).strip()
        shutil.copy2(img_map[img_name.lower()], img_dir / img_name)
