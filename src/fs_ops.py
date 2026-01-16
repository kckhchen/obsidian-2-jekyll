from pathlib import Path
from .templates import CALLOUT_CSS
from . import settings


def build_img_map(dir):
    extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}
    img_map = {}
    for p in dir.rglob("*"):
        if p.is_file() and p.suffix.lower() in extensions:
            img_map[p.name.lower()] = p

    return img_map


def setup_dir(post_dir, img_dir, dry):
    for path in [post_dir, img_dir]:
        if not path.exists():
            print(f"---- Destination folder not found, creating {path} ----")
            if not dry:
                path.mkdir(parents=True, exist_ok=True)


def ensure_css_exists(css_name, dry):
    includes_dir = Path(settings.config.JEKYLL_DIR) / settings.config.INCLUDES_FOLDER
    css_path = includes_dir / css_name
    if not css_path.exists():
        print(f"---- Creating default callout CSS at: {css_path} ----")
        if not dry:
            css_path.parent.mkdir(parents=True, exist_ok=True)
            css_path.write_text(CALLOUT_CSS, encoding="utf-8")


def announce_paths(source_dir, post_dir, dry):
    if dry:
        print("------------ DRY RUN MODE -------------")
        print("Operations will be printed but files won't be changed.\n")

    print(f"Start processing posts in folder [ {source_dir} ]...")
    print(f"Destination path: [ {post_dir} ]\n")
