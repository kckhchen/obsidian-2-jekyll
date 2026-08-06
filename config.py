import os
import sys

from dotenv import load_dotenv

load_dotenv()

try:
    VAULT_DIR = os.environ["VAULT_DIR"]
    JEKYLL_DIR = os.environ["JEKYLL_DIR"]
except KeyError as e:
    print(f"STARTUP FAILED: Missing required environment variable: {e}")
    sys.exit(1)


MATH_RENDERING_MODE = os.environ.get("MATH_RENDERING_MODE", "inject_cdn")
PREVENT_DOUBLE_BASEURL = os.environ.get("PREVENT_DOUBLE_BASEURL", str(False))
INCLUDES_FOLDER = os.environ.get("INCLUDES_FOLDER", "_includes")
POST_FOLDER = os.environ.get("POST_FOLER", "_posts")
IMG_FOLDER = os.environ.get("IMG_FOLDER", "assets/images/obsidian")
