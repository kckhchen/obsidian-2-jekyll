# path to the folder inside your vault for posts ready to publish.
# note: all posts inside SOURCE_DIR will be published.
# posts outside of this folder will not be published.
SOURCE_DIR = "/User/me/path/to/my-vault/published"

# path to your Jekyll website's directory
JEKYLL_DIR = "/Users/me/path/to/my/jekyll/project"

# The image folder in your Jekyll project folder
IMG_FOLDER = "assets/images"


# ---------------- More Settings -----------------------

# If the Jekyll theme supports math rendering and can recognize "math: true"
# please uncomment "metadata".
# If the Jekyll theme does not support math rendering
# or you want to inject mathjax cdn, please uncomment "inject_cdn"

# MATH_RENDERING_MODE = "metadata"
MATH_RENDERING_MODE = "inject_cdn"

# Only switch this to "True" if you are using Jekyll 4.X or newer versions AND you use a baseurl.
# This is due to a change of how {% link %} works after Jekyll 4.X
PREVENT_DOUBLE_BASEURL = False

# These are the default paths for Jekyll
POST_FOLDER = "_posts"
INCLUDES_FOLDER = "_includes"

try:
    from config_local import *
except ImportError:
    pass
