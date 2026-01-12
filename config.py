# path to the folder inside your vault for posts ready to publish.
# note: all posts inside POST_FOLDER will be published.
# posts outside of this folder will not be published.
SOURCE_DIR = "./examples/Example-Vault/example-posts"

# desired path to store the processed posts and the associated images.
POST_DEST = "./_posts"
IMG_DEST = "./assets/images"

# absolute path for Jekyll to locate the image folder
# (please change this path to your image path. This is for the demo website.)
IMG_LINK = "/obsidian-2-jekyll/assets/images"

# If the Jekyll theme supports math rendering and can recognize "math: true"
# please uncomment "metadata".
# If the Jekyll theme does not support math rendering
# or you want to inject mathjax cdn, please uncomment "inject_cdn"

# MATH_RENDERING_MODE = "metadata"
MATH_RENDERING_MODE = "inject_cdn"
