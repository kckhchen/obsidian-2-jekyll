from pathlib import Path

from config import IMG_FOLDER, INCLUDES_FOLDER, JEKYLL_DIR, POST_FOLDER, VAULT_DIR

from .patterns import IMG_EXT
from .templates import CALLOUT_CSS


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


def announce_paths(vault_dir, post_dir, dry):
    if dry:
        print("------------ DRY RUN MODE -------------")
        print("Operations will be printed but files won't be changed.\n")

    print(f"Start processing posts in Vault [ {vault_dir} ]...")
    print(f"Destination path: [ {post_dir} ]\n")


def make_paths():
    vault_dir = Path(VAULT_DIR)
    post_dir, img_dir = [
        Path(JEKYLL_DIR) / folder for folder in (POST_FOLDER, IMG_FOLDER)
    ]
    return vault_dir, post_dir, img_dir
