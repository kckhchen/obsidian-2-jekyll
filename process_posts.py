import os
import re
import shutil

VAULT_DIR = "/Users/casey/Library/Mobile Documents/iCloud~md~obsidian/Documents/Casey"
POST_DIR_NAME = "_published"
IMG_DIR_NAME = "_images"

POST_DIR = f"/Users/casey/Library/Mobile Documents/iCloud~md~obsidian/Documents/Casey/{POST_DIR_NAME}"
IMG_DIR = f"/Users/casey/Library/Mobile Documents/iCloud~md~obsidian/Documents/Casey/{IMG_DIR_NAME}"
POST_DIST = "./dist/posts"
IMG_DIST = "./dist/images"


def build_file_map(root_dir):
    # list all files in post and img folders
    file_map = {}
    for root, dirs, files in os.walk(root_dir):
        if POST_DIR_NAME in root or IMG_DIR_NAME in root:
            for filename in files:
                file_map[filename.lower()] = os.path.join(root, filename)
    return file_map


def clean_and_copy():
    # re-create the dist folders
    if os.path.exists("./dist"):
        shutil.rmtree("./dist")
    os.makedirs(POST_DIST)
    os.makedirs(IMG_DIST)

    if not os.path.exists(POST_DIR):
        print(f"Post source folder {POST_DIR} not found.")
        return

    for root, dirs, files in os.walk(POST_DIR):
        for filename in files:
            if not filename.endswith(".md"):
                continue

            filepath = os.path.join(root, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            fm_match = re.search(r"---\n(.*?)\n---", content, flags=re.DOTALL)
            if not fm_match:
                continue
            frontmatter = fm_match.group(1)

            # check for dates in frontmatter and prepend the filename
            date_match = re.search(r"date:\s*(\d{4}-\d{2}-\d{2})", frontmatter)
            if not date_match:
                continue

            date_str = date_match.group(1)
            clean_name = filename.replace(" ", "-").lower()

            if not clean_name.startswith(date_str):
                new_filename = f"{date_str}-{clean_name}"
            else:
                new_filename = clean_name

            # extract h1 title from markdown and add to frontmatter
            fm_end_pos = fm_match.end()
            h1_match = re.search(
                r"^\s*#\s+(.+?)$", content[fm_end_pos:], flags=re.MULTILINE
            )
            if h1_match:
                h1_title = h1_match.group(1).strip()
                if "title:" not in frontmatter:
                    frontmatter += f"\ntitle: {h1_title}"
                content = content[:fm_end_pos] + re.sub(
                    r"^\s*#\s+.+?\n",
                    "",
                    content[fm_end_pos:],
                    count=1,
                    flags=re.MULTILINE,
                )

            # convert lang/language into categories: [zh] or [en]
            lang_match = re.search(
                r'^\s*(?:lang):\s*"?([A-Za-z]{2})"?\s*$',
                frontmatter,
                flags=re.IGNORECASE | re.MULTILINE,
            )
            if lang_match:
                lang = lang_match.group(1).lower()
                if lang in ("zh", "en"):
                    # replace existing categories line if present, otherwise append
                    if re.search(
                        r"^\s*categories:\s*\[.*?\]\s*$",
                        frontmatter,
                        flags=re.MULTILINE,
                    ):
                        frontmatter = re.sub(
                            r"^\s*categories:\s*\[.*?\]\s*$",
                            f"categories: [{lang}]",
                            frontmatter,
                            flags=re.MULTILINE,
                        )
                    elif re.search(
                        r"^\s*categories:\s*.*$", frontmatter, flags=re.MULTILINE
                    ):
                        frontmatter = re.sub(
                            r"^\s*categories:\s*.*$",
                            f"categories: [{lang}]",
                            frontmatter,
                            flags=re.MULTILINE,
                        )
                    else:
                        frontmatter += f"\ncategories: [{lang}]"
                    # remove the lang line to avoid duplication
                    frontmatter = re.sub(
                        r'^\s*(?:lang|language):\s*"?' + re.escape(lang) + '"?\s*$',
                        "",
                        frontmatter,
                        flags=re.IGNORECASE | re.MULTILINE,
                    )
                    # normalize blank lines
                    frontmatter = re.sub(r"\n{2,}", "\n", frontmatter).strip()

            # look for ![[img.file]] and change to ![](/assets/images/img.file)
            # if img not found just preserve the original
            vault_images = build_file_map(IMG_DIR)

            def img_replacer(match):
                raw_name = match.group(1).strip()
                lower_name = raw_name.lower()
                if lower_name in vault_images:
                    src_path = vault_images[lower_name]
                    dest_path = os.path.join(IMG_DIST, raw_name)
                    shutil.copy2(src_path, dest_path)
                    return f"![](/assets/images/{raw_name})"
                else:
                    return match.group(0)

            content = re.sub(r"!\[\[(.*?)(?:\|.*?)?\]\]", img_replacer, content)

            # find math expressions and make is render-able

            def math_block_replacer(match):
                inner_math = match.group(1)

                # change \\ to \\\\\\\\ so that MD will show \\\\ and html will read \\
                # which is important for math block line break
                fixed_math = inner_math.replace(r"\\", r"\\\\\\\\")

                # if math block starts with \begin{...} return the raw math block
                # (i.e. strip away $$...$$ since \begin{} is a math block itself)
                # else simply swap $$...$$ for \[...\] and apply pretty line breaks
                if re.match(r"^\s*\\begin\{.+?\}", fixed_math.strip()):
                    return fixed_math
                else:
                    return f"\n\\\[{fixed_math}\\\]\n"

            use_mathjax = 1 if re.search(r'\s*math:\s*"?true"?\s*', frontmatter) else 0

            if use_mathjax:
                # look for math block and apply changes first
                content = re.sub(
                    r"\$\$(.*?)\$\$", math_block_replacer, content, flags=re.DOTALL
                )
                # replace $...$ to \(...\)
                content = re.sub(
                    r"(?<!\\)\$([^$]+?)(?<!\\)\$", r"\\\\(\1\\\\)", content
                )
                # add this line at the end for html to recognize
                content += "\n\n{% include mathjax.html %}"

            # write the treated content into the dist folder waiting to be uploaded
            # and change the name to new_filename i.e. yyyy-mm-dd-post-name.md
            final_content = f"---\n{frontmatter}\n---\n{content[fm_match.end():]}"
            with open(
                os.path.join(POST_DIST, new_filename), "w", encoding="utf-8"
            ) as f:
                f.write(final_content)
                print(f"Processed: {new_filename}, use_math = {use_mathjax}")


if __name__ == "__main__":
    clean_and_copy()
