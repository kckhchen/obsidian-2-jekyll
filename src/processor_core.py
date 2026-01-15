import frontmatter

from .utils import get_dest_fpath, shield_content, unshield
from .fs_ops import announce_paths, setup_dir, ensure_css_exists, build_img_map
from .text_cleanup import process_h1, strip_comments
from .process_math import process_math
from .process_images import process_embedded_images
from .process_links import process_wikilinks
from .process_callouts import process_callouts


def process_posts(source_dir, post_dir, img_dir, dry, layout):
    announce_paths(source_dir, post_dir, dry)
    setup_dir(post_dir, img_dir, dry)
    ensure_css_exists("obsidian-callouts.html", dry)
    img_map = build_img_map(source_dir.parent)
    skipped = 0

    for source_fpath in source_dir.rglob("*.md"):
        post = frontmatter.load(source_fpath)
        dest_fpath = get_dest_fpath(post, source_fpath, post_dir)
        filename, new_fname = source_fpath.name, dest_fpath.name
        if _should_proceed(source_fpath, dest_fpath):
            print(f"Processing: {filename} -> {new_fname}")
            if not dry:
                post = _process_single_post(post, source_dir, img_map, img_dir, layout)
                frontmatter.dump(post, dest_fpath)
        else:
            skipped += 1

    print(f"\nProcessing finished. Skipped {skipped} unchanged files.")


def _should_proceed(source_fpath, dest_fpath):
    if not dest_fpath.exists():
        return True

    return source_fpath.stat().st_mtime > dest_fpath.stat().st_mtime


def _process_single_post(post, source_dir, img_map, img_dir, layout):
    post, code_blocks = shield_content(post, mode="code")
    post, url_blocks = shield_content(post, mode="url")
    post, math_blocks = shield_content(post, mode="math")

    post = process_h1(post, layout)
    post = strip_comments(post)
    post = process_embedded_images(post, img_map, img_dir)
    post = process_wikilinks(post, source_dir)
    post = process_callouts(post)

    post = unshield(post, math_blocks)
    post = process_math(post)

    post = unshield(post, url_blocks)
    post = unshield(post, code_blocks)
    return post
