import os
from pathlib import Path
from processor import parse_md_file, get_dist_filepath


def remove_stale_files(post_dist, post_dir):
    print(f"\nStarting cleaning up process in folder [ {post_dist} ]...\n")
    obs_formatted_filenames = get_obs_formatted_filenames(post_dist, post_dir)
    to_be_removed = list_files_to_be_removed(post_dist, obs_formatted_filenames)
    if to_be_removed:
        remove_files(post_dist, to_be_removed)
    else:
        print("No stale files found. Nothing will be removed.")


def get_obs_formatted_filenames(post_dist, post_dir):
    formatted_filename_list = []
    for root, _, files in os.walk(post_dir):
        for filename in files:
            if filename.endswith(".md"):
                _, frontmatter, _ = parse_md_file(root, filename)
                filename, _ = get_dist_filepath(root, filename, frontmatter, post_dist)
                formatted_filename_list.append(filename)
    return formatted_filename_list


def list_files_to_be_removed(post_dist, current_posts):
    to_be_removed = []
    for f in Path(post_dist).iterdir():
        if f.is_file() and f.name.endswith(".md"):
            filename = f.name
            if filename not in current_posts:
                to_be_removed.append(filename)
    return to_be_removed


def remove_files(dist, file_list):
    print("The following files will be removed:\n")
    for name in file_list:
        print(name)

    if input("\nConfirm removal? [y/n]: ") == "y":
        for name in file_list:
            os.remove(os.path.join(dist, name))
        print("Files are removed.")
    else:
        print("Process aborted.")
