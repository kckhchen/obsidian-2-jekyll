import re
from pathlib import Path
from datetime import datetime


def get_dest_filepath(post, source_path, post_dest=None):
    date_val = post.get("date")
    if date_val:
        date_str = str(date_val)[:10]
    else:
        date_str = get_creation_time(source_path)

    clean_stem = re.sub(r"^\d{4}-\d{2}-\d{2}[-_]?", "", source_path.stem)
    new_name = f"{date_str}-{slugify(clean_stem)}{source_path.suffix}"

    if post_dest is not None:
        return post_dest / new_name
    else:
        return new_name


def get_creation_time(filepath):
    stat = Path(filepath).stat()
    timestamp = getattr(stat, "st_birthtime", getattr(stat, "st_ctime", stat.st_mtime))
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")


def slugify(name):
    return re.sub(r"[^a-zA-Z0-9.]+", "-", name).strip("-").lower()


def validate_inputs(source_dir):
    if not source_dir.exists():
        print(f"Error: Source folder '{source_dir}' not found.")
        return False
    return True
