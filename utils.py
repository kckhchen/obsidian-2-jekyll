import re
import frontmatter
from pathlib import Path
from datetime import datetime


def parse_md_file(root, filename):
    source_path = Path(root) / filename
    post = frontmatter.load(source_path)
    return source_path, post


def get_dest_filepath(source_path, filename, post, dest_path):
    date_str = post.get("date") or get_creation_time(source_path)
    file_obj = Path(filename)
    slug = slugify(re.sub(r"^\d{4}-\d{2}-\d{2}-", "", file_obj.stem))
    new_name = f"{date_str}-{slug}{file_obj.suffix}"
    return new_name, Path(dest_path) / new_name


def get_creation_time(filepath):
    stat = Path(filepath).stat()
    timestamp = getattr(stat, "st_birthtime", getattr(stat, "st_ctime", stat.st_mtime))
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")


def slugify(name):
    return re.sub(r"[^a-zA-Z0-9.]+", "-", name).strip("-").lower()
