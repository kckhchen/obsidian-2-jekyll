import os
import sys
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

_vault_str = os.environ.get("VAULT_DIR", None)
_jekyll_str = os.environ.get("JEKYLL_DIR", None)

VAULT_DIR = Path(_vault_str) if _vault_str else None
JEKYLL_DIR = Path(_jekyll_str) if _jekyll_str else None

POST_FOLDER = Path(os.environ.get("POST_FOLDER", "_posts"))
IMG_FOLDER = Path(os.environ.get("IMG_FOLDER", "assets/images/obsidian"))
POST_DIR = JEKYLL_DIR / POST_FOLDER if JEKYLL_DIR else None
IMG_DIR = JEKYLL_DIR / IMG_FOLDER if JEKYLL_DIR else None

MATH_RENDERING_MODE = os.environ.get("MATH_RENDERING_MODE", "inject_cdn")
PREVENT_DOUBLE_BASEURL = (
    os.environ.get("PREVENT_DOUBLE_BASEURL", str(False)).lower() == "true"
)
INCLUDES_FOLDER = os.environ.get("INCLUDES_FOLDER", "_includes")


def validate_config():
    if VAULT_DIR is None or not Path(VAULT_DIR).exists():
        print(f"STARTUP FAILED: VAULT_DIR doesn't exist: {VAULT_DIR}")
        sys.exit(1)

    if JEKYLL_DIR is None or not Path(JEKYLL_DIR).exists():
        print(f"STARTUP FAILED: JEKYLL_DIR doesn't exist: {JEKYLL_DIR}")
        sys.exit(1)
