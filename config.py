# path to the folder inside your vault for posts ready to publish.
# note: all posts inside SOURCE_DIR will be published.
# posts outside of this folder will not be published.
SOURCE_DIR = "/User/me/path/to/my/vault"

# path to your Jekyll website's directory
JEKYLL_DIR = "/Users/me/path/to/my/jekyll/project"

# absolute path for Jekyll to locate the image folder
# (please change this path to your image path. This is for the demo website.)
IMG_FOLDER = "assets/images"
IMG_URL_PREFIX = "/for/example/obsidian-2-jekyll/"

# If the Jekyll theme supports math rendering and can recognize "math: true"
# please uncomment "metadata".
# If the Jekyll theme does not support math rendering
# or you want to inject mathjax cdn, please uncomment "inject_cdn"

# MATH_RENDERING_MODE = "metadata"
MATH_RENDERING_MODE = "inject_cdn"

# ------------------------------------------------------

# These are the default paths for Jekyll
POST_FOLDER = "_posts"
INCLUDES_FOLDER = "_includes"

try:
    from config_local import *
except ImportError:
    pass
