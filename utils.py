import os
import shutil


def build_file_map(directory):
    file_map = {}
    for root, _, files in os.walk(directory):
        for f in files:
            file_map[f.lower()] = os.path.join(root, f)
    return file_map


def setup_dir(post_dist, img_dist):
    if os.path.exists(post_dist):
        shutil.rmtree(post_dist)
    if os.path.exists(img_dist):
        shutil.rmtree(img_dist)
    os.makedirs(post_dist, exist_ok=True)
    os.makedirs(img_dist, exist_ok=True)
