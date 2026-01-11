import os
from config import *
from utils import build_file_map, setup_dir
from processor import parse_md_file, update_filename
from transformers import process_h1, process_images, process_wikilinks, process_math
from processor import write_to_file


def main():
    setup_dir(POST_DIST, IMG_DIST)

    post_dir = os.path.join(VAULT_DIR, POST_FOLDER)
    img_dir = os.path.join(VAULT_DIR, IMG_FOLDER)
    img_map = build_file_map(img_dir)

    for root, _, files in os.walk(post_dir):
        for filename in files:
            frontmatter, body = parse_md_file(root, filename)

            if not frontmatter is None:
                new_filename = update_filename(root, filename, frontmatter)
                body, frontmatter = process_h1(body, frontmatter, LAYOUT)
                body = process_images(body, img_map, IMG_DIST, IMG_LINK)
                body = process_wikilinks(body)
                body = process_math(body)

                write_to_file(POST_DIST, new_filename, frontmatter, body)


if __name__ == "__main__":
    main()
