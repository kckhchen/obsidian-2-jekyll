import os
import shutil

IMG_EXT = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp")


def build_file_map(directory):
    file_map = {}
    for root, _, files in os.walk(directory):
        for f in files:
            if f.lower().endswith(IMG_EXT):
                file_map[f.lower()] = os.path.join(root, f)
    return file_map


def setup_dir(post_dist, img_dist):
    if not os.path.exists(post_dist):
        os.makedirs(post_dist, exist_ok=True)
        print(f"destination post folder not found, creating {post_dist}...")
    if not os.path.exists(img_dist):
        os.makedirs(img_dist, exist_ok=True)
        print(f"destination image folder not found, creating {img_dist}...")


def should_proceed(source_path, dest_path):
    if not os.path.exists(dest_path):
        return True

    return os.path.getmtime(source_path) > os.path.getmtime(dest_path)
