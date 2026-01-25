import re


def process_h1(post, layout="post"):
    post["layout"] = post.get("layout") or layout
    h1_pattern = r"^\s*#\s+(?P<h1>.+?)$"
    h1_match = re.search(h1_pattern, post.content, flags=re.MULTILINE)

    if h1_match:
        title = h1_match.group("h1").strip()
        post["title"] = post.get("title") or title
        post.content = re.sub(
            h1_pattern, "", post.content, count=1, flags=re.MULTILINE
        ).strip()
    return post


def strip_comments(post):
    comment_pattern = r"%%.*?%%"
    post.content = re.sub(comment_pattern, "", post.content, flags=re.DOTALL)
    return post


def process_highlights(post):
    highlight_pattern = r"==(.*?)=="
    post.content = re.sub(
        highlight_pattern, "<mark>" + r"\g<1>" + "</mark>", post.content
    )
    return post


def ensure_table_spacing(post):
    pattern = r"(?<!\n)\n(\|.*\|\n\|[\s:-]+\|)"
    post.content = re.sub(pattern, r"\n\n\1", post.content)
    return post
