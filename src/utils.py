import re
from pathlib import Path
from datetime import datetime
import frontmatter


def get_creation_time(filepath):
    stat = Path(filepath).stat()
    timestamp = getattr(stat, "st_birthtime", getattr(stat, "st_ctime", stat.st_mtime))
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")


def slugify(name):
    return re.sub(r"[^a-zA-Z0-9.]+", "-", name).strip("-").lower()


def validate_configs(vault_dir, config):
    valid_modes = ["metadata", "inject_cdn"]
    mode = config.MATH_RENDERING_MODE
    if not vault_dir.exists():
        raise FileNotFoundError(f"Error: Vault '{vault_dir}' not found.")

    if mode not in valid_modes:
        raise ValueError(
            f"Invalid MATH_RENDERING_MODE: '{config.MATH_RENDERING_MODE}'. "
            f"Must be one of: {valid_modes}."
        )


def shield_content(post, mode):

    def _replacer(match):
        key = f"&&{mode.upper()}_{len(stash)}&&"
        stash[key] = match.group(0)
        return key

    if mode == "code":
        pattern = r"(```[\s\S]*?```|`[^`\n]+`)"
    elif mode == "math":
        pattern = r"(\$\$[\s\S]*?\$\$|(?<!\$)\$[^$]+\$(?!\$))"
    elif mode == "url":
        pattern = r"https?://[^)\s]+"
    else:
        raise ValueError(f"Unknown shield type: {mode}")

    stash = {}
    post.content = re.sub(pattern, _replacer, post.content)
    return post, stash


def unshield(post, stash):
    for key, original_text in stash.items():
        post.content = post.content.replace(key, original_text)
    return post


def get_valid_files(vault_dir, post_dir):
    valid_files = {}

    for path in vault_dir.rglob("*.md"):
        try:
            with open(path, "r", encoding="utf-8") as f:

                if f.readline().strip() != "---":
                    continue

                f.seek(0)
                post = frontmatter.load(f)

                if str(post.get("share")).lower() == "true":
                    dest_path = _get_dest_fpath(post, path, post_dir)

                    if path.stem in valid_files:
                        print(
                            f"Warning: Duplicate filename found: '{path.stem}'. {path} will be skipped."
                        )
                        continue

                    valid_files[path.stem] = {
                        "source_path": path,
                        "dest_path": dest_path,
                    }

        except Exception as e:
            print(f"Warning: Could not process '{path.name}'. {e}")
            continue

    return valid_files


def _get_dest_fpath(post, source_fpath, post_dir):
    date_val = post.get("date")
    if date_val:
        date_str = str(date_val)[:10]
    else:
        date_str = get_creation_time(source_fpath)

    clean_stem = re.sub(r"^\d{4}-\d{2}-\d{2}[-_]?", "", source_fpath.stem)
    new_name = f"{date_str}-{slugify(clean_stem)}{source_fpath.suffix}"

    return post_dir / new_name
