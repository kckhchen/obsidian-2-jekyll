import re
import frontmatter
from pathlib import Path
from processor import get_dest_filepath


def remove_stale_files(post_dir, post_dest, img_dest):
    print(f"\nStarting cleaning up process...")
    print(f"Post folder: [ {post_dest} ]")
    print(f"Image folder: [ {img_dest} ]\n")
    obs_formatted_filenames, all_post_images = scan_source_files(post_dir)
    to_be_removed = list_posts_to_be_removed(
        post_dest, obs_formatted_filenames
    ) + list_imgs_to_be_removed(img_dest, all_post_images)

    if to_be_removed:
        remove_files(to_be_removed)
    else:
        print("No stale files found. Nothing will be removed.")


def scan_source_files(post_dir):
    formatted_filenames = set()
    all_images = set()

    for source_path in post_dir.rglob("*.md"):
        post = frontmatter.load(source_path)
        filename = get_dest_filepath(post, source_path)
        formatted_filenames.add(filename)

        img_list = scan_post_images(post)
        all_images.update(img_list)

    return formatted_filenames, all_images


def list_posts_to_be_removed(post_dest, current_posts):
    to_be_removed = []
    for f in Path(post_dest).iterdir():
        if f.is_file() and re.match(r"\d{4}-\d{2}-\d{2}-.+\.md", f.name):
            filename = f.name
            if filename not in current_posts:
                to_be_removed.append(Path(post_dest) / filename)
    return to_be_removed


def list_imgs_to_be_removed(img_dest, all_post_images):
    img_ext = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp")
    to_be_removed = []
    for img in Path(img_dest).iterdir():
        if img.is_file() and img.suffix in img_ext:
            filename = img.name
            if filename not in all_post_images:
                to_be_removed.append(Path(img_dest) / filename)
    return to_be_removed


def remove_files(file_path_list):
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


def scan_post_images(post):
    img_pattern = r"!\[\[(?P<wiki>[^|\]]+).*?\]\]|!\[[^\]]*\]\((?P<md>[^)]+)\)"

    def extract_filename(match):
        path_str = match.group("wiki") or match.group("md")
        if match.group("md") and path_str.startswith(("http:", "https:")):
            return None

        return Path(path_str).name

    img_list = [
        name
        for match in re.finditer(img_pattern, post.content)
        if (name := extract_filename(match))
    ]

    return img_list


if __name__ == "__main__":
    remove_stale_files(
        "/Users/casey/Dev/obsidian-2-jekyll/examples/Example-Vault/example-posts",
        "/Users/casey/Dev/obsidian-2-jekyll/_posts",
        "/Users/casey/Dev/obsidian-2-jekyll/assets/images",
    )
