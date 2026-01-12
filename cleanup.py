import os
from pathlib import Path
from processor import parse_md_file, get_dest_filepath


def remove_stale_files(post_dest, post_dir):
    print(f"\nStarting cleaning up process in folder [ {post_dest} ]...\n")
    obs_formatted_filenames = get_obs_formatted_filenames(post_dest, post_dir)
    to_be_removed = list_files_to_be_removed(post_dest, obs_formatted_filenames)
    if to_be_removed:
        remove_files(post_dest, to_be_removed)
    else:
        print("No stale files found. Nothing will be removed.")


def get_obs_formatted_filenames(post_dest, post_dir):
    formatted_filename_list = []
    for root, _, files in os.walk(post_dir):
        for filename in files:
            if filename.endswith(".md"):
                source_path, post = parse_md_file(root, filename)
                new_filename, _ = get_dest_filepath(
                    source_path, filename, post, post_dest
                )
                formatted_filename_list.append(new_filename)
    return formatted_filename_list


def list_files_to_be_removed(post_dest, current_posts):
    to_be_removed = []
    for f in Path(post_dest).iterdir():
        if f.is_file() and f.name.endswith(".md"):
            filename = f.name
            if filename not in current_posts:
                to_be_removed.append(filename)
    return to_be_removed


def remove_files(dir, file_list):
    print("The following files will be removed:\n")
    for name in file_list:
        print(name)

    if input("\nConfirm removal? [y/n]: ") == "y":
        for name in file_list:
            os.remove(os.path.join(dir, name))
        print("Files are removed.")
    else:
        print("Process aborted.")
