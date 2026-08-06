import re
from pathlib import Path

import frontmatter

from src.process_callouts import process_callouts
from src.process_images import process_embedded_images
from src.process_links import process_wikilinks
from src.process_math import process_math
from src.text_cleanup import text_cleanup
from src.utils import shield_content, unshield


def process_posts(files, img_map, img_dir, dry, layout, force, only=None):
    try:
        skipped = 0
        for src, dest, post in sorted(_iter_files(files, only)):
            reason = _should_proceed(src, dest, force)

            if reason:
                print(f"{reason}: {Path(src.parent.name) / src.name} -> {dest.name}")

                if not dry:
                    post, code_blocks = shield_content(post, mode="code")
                    post, url_blocks = shield_content(post, mode="url")
                    post, math_blocks = shield_content(post, mode="math")

                    post = text_cleanup(post, layout)
                    post = process_embedded_images(post, img_map, img_dir)
                    post = process_wikilinks(post, files)
                    post = process_callouts(post)

                    post = unshield(
                        post, math_blocks, lambda x: re.sub(r"\|", r" \\vert ", x)
                    )
                    post = process_math(post)

                    post = unshield(post, url_blocks)
                    post = unshield(post, code_blocks)
                    frontmatter.dump(post, dest)
            else:
                skipped += 1

    except (ValueError, FileNotFoundError) as e:
        print(e)
        return

    print(f"\nProcessing finished. Skipped {skipped} unchanged files.")


def _should_proceed(src, dest, force):
    if force:
        return "Force Updating"

    if not dest.exists():
        return "Creating"

    if src.stat().st_mtime > dest.stat().st_mtime:
        return "Updating"

    return False


def _iter_files(files, only_file=None):
    if only_file:
        filename = Path(only_file).stem

        if filename not in files:
            raise ValueError(f"Error: Cannot find '{only_file}' (share: true needed).")

        src = files[filename]["source_path"]
        dest = files[filename]["dest_path"]
        post = frontmatter.load(src)
        yield src, dest, post

    else:
        for data in files.values():
            src = data["source_path"]
            dest = data["dest_path"]
            post = frontmatter.load(src)
            yield src, dest, post
