# Path to your Obsidian Vault.
VAULT_DIR = "/User/me/path/to/obsidian-vault"

# Path to your Jekyll website's directory.
JEKYLL_DIR = "/Users/me/path/to/my/jekyll-project"

# ---------------- More Settings -----------------------

# If the Jekyll theme supports math rendering and can recognize "math: true"
# please uncomment "metadata".
# If the Jekyll theme does not support math rendering
# or you want to inject mathjax cdn, please uncomment "inject_cdn"

# MATH_RENDERING_MODE = "metadata"
MATH_RENDERING_MODE = "inject_cdn"

# Only switch this to True if you are using Jekyll 4.X or newer versions
# and you see duplicate baseurls in your internal links.
# This is due to a change of how {% link %} works after Jekyll 4.0.
PREVENT_DOUBLE_BASEURL = False

# These are the default paths for Jekyll.
# Do not change this unless necessary.
POST_FOLDER = "_posts"
INCLUDES_FOLDER = "_includes"
IMG_FOLDER = "assets/images"

# You can also create a config_local.py to store your configs.
# Those values will be prioritized by the tool.

try:
    from config_local import *
except ImportError:
    pass
