import re
import frontmatter
from pathlib import Path


def remove_stale_files(valid_files, post_dir, img_dir):
    print(f"\nStarting cleaning up process...")
    print(f"Post folder: [ {post_dir} ]")
    print(f"Image folder: [ {img_dir} ]\n")

    all_post_images = _get_post_images(valid_files)
    to_be_removed = _list_posts_to_be_removed(
        post_dir, valid_files
    ) + _list_imgs_to_be_removed(img_dir, all_post_images)

    if to_be_removed:
        _remove_files(to_be_removed)
    else:
        print("No stale files found. Nothing will be removed.")


def _get_post_images(valid_files):
    all_images = set()

    for data in valid_files.values():
        src = data["source_path"]
        post = frontmatter.load(src)
        img_list = _scan_post_images(post)
        all_images.update(img_list)

    return all_images


def _list_posts_to_be_removed(post_dir, valid_files):
    to_be_removed = []
    current_posts = [data["dest_path"].name for data in valid_files.values()]

    for f in Path(post_dir).iterdir():
        if f.is_file() and re.match(r"\d{4}-\d{2}-\d{2}-.+\.md", f.name):
            filename = f.name

            if filename not in current_posts:
                to_be_removed.append(Path(post_dir) / filename)

    return to_be_removed


def _list_imgs_to_be_removed(img_dir, all_post_images):
    img_ext = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp")
    to_be_removed = []

    for img in Path(img_dir).iterdir():
        if img.is_file() and img.suffix in img_ext:
            filename = img.name

            if filename not in all_post_images:
                to_be_removed.append(Path(img_dir) / filename)
    return to_be_removed


def _remove_files(file_path_list):
    if not file_path_list:
        return

    print("The following files will be removed:\n")
    for p in file_path_list:
        print(f"[{p.parent.name}] {p.name}")

    if input("\nConfirm removal? [y/n]: ").lower() == "y":
        for p in file_path_list:
            try:
                p.unlink()
            except FileNotFoundError:
                print(f"Skipped {p.name} (not found)")
        print("Files removed.")
    else:
        print("Process aborted.")


def _scan_post_images(post):
    img_pattern = r"!\[\[(?P<wiki>[^|\]]+).*?\]\]|!\[[^\]]*\]\((?P<md>[^)]+)\)"

    img_list = [
        name
        for match in re.finditer(img_pattern, post.content)
        if (name := _extract_filename(match))
    ]

    return img_list


def _extract_filename(match):
    path_str = match.group("wiki") or match.group("md")
    if match.group("md") and path_str.startswith(("http:", "https:")):
        return None

    return Path(path_str).name
