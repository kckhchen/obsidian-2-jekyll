import os
import re
from datetime import datetime


def parse_md_file(root, filename):
    source_path = os.path.join(root, filename)
    content = open(source_path, "r", encoding="utf-8").read()
    fm_match = re.search(r"^---\n(.*?)\n---\n", content, flags=re.DOTALL)
    if not fm_match:
        return source_path, "", content
    return source_path, fm_match.group(1), content[fm_match.end() :]


def get_dist_filepath(root, filename, frontmatter, dist_path):
    stat_info = os.stat(os.path.join(root, filename))
    creation_date = datetime.fromtimestamp(stat_info.st_birthtime).strftime("%Y-%m-%d")
    date_match = re.search(r"date:\s*(\d{4}-\d{2}-\d{2})", frontmatter)
    date_str = date_match.group(1) if date_match else creation_date
    clean_name = re.sub(r"\d{4}-\d{2}-\d{2}-", "", filename).replace(" ", "-").lower()
    new_name = f"{date_str}-{clean_name}"
    return new_name, os.path.join(dist_path, new_name)


def write_to_file(filepath, frontmatter, body):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"---\n{frontmatter.strip()}\n---\n\n{body.strip()}")
