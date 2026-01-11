import os
from config import *
from utils import build_file_map, setup_dir, should_proceed
from processor import parse_md_file, get_dist_filepath
from transformers import process_h1, process_images, process_wikilinks, process_math
from processor import write_to_file


def main():
    setup_dir(POST_DIST, IMG_DIST)

    post_dir = os.path.join(VAULT_DIR, POST_FOLDER)
    img_map = build_file_map(VAULT_DIR)

    for root, _, files in os.walk(post_dir):
        for filename in files:
            frontmatter, body = parse_md_file(root, filename)
            source_path = os.path.join(root, filename)

            if not frontmatter is None:
                new_filepath = get_dist_filepath(root, filename, frontmatter, POST_DIST)
                if should_proceed(source_path, new_filepath):
                    print(f"Processing: {filename} -> {new_filepath}")
                    body, frontmatter = process_h1(body, frontmatter, LAYOUT)
                    body = process_images(body, img_map, IMG_DIST, IMG_LINK)
                    body = process_wikilinks(body)
                    body = process_math(body)

                    write_to_file(new_filepath, frontmatter, body)
                else:
                    print(f"Skipping (Unchanged): {filename}")

            else:
                print(f"Skipping (Not an md file): {filename}")


if __name__ == "__main__":
    main()
