import os
import sys
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

try:
    VAULT_DIR = os.environ["VAULT_DIR"]
    JEKYLL_DIR = os.environ["JEKYLL_DIR"]
except KeyError as e:
    print(f"STARTUP FAILED: Missing required environment variable: {e}")
    sys.exit(1)

VAULT_DIR = Path(VAULT_DIR)
JEKYLL_DIR = Path(JEKYLL_DIR)

if not VAULT_DIR.exists():
    raise FileNotFoundError(f"Cannot file {VAULT_DIR}.")
if not JEKYLL_DIR.exists():
    raise FileNotFoundError(f"Cannot file {JEKYLL_DIR}.")

POST_FOLDER = Path(os.environ.get("POST_FOLER", "_posts"))
IMG_FOLDER = Path(os.environ.get("IMG_FOLDER", "assets/images/obsidian"))
POST_DIR = JEKYLL_DIR / POST_FOLDER
IMG_DIR = JEKYLL_DIR / IMG_FOLDER


MATH_RENDERING_MODE = os.environ.get("MATH_RENDERING_MODE", "inject_cdn")
PREVENT_DOUBLE_BASEURL = (
    os.environ.get("PREVENT_DOUBLE_BASEURL", str(False)).lower() == "true"
)
INCLUDES_FOLDER = os.environ.get("INCLUDES_FOLDER", "_includes")
