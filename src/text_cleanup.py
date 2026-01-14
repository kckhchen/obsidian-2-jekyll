import re


def process_h1(post, layout="post"):
    post["layout"] = post.get("layout") or layout
    h1_pattern = r"^\s*#\s+(.+?)$"
    h1_match = re.search(h1_pattern, post.content, flags=re.MULTILINE)

    if h1_match:
        title = h1_match.group(1).strip()
        post["title"] = post.get("title") or title
        post.content = re.sub(
            h1_pattern, "", post.content, count=1, flags=re.MULTILINE
        ).strip()
    return post


def strip_comments(post):
    comment_pattern = r"%%.*?%%"
    post.content = re.sub(comment_pattern, "", post.content, flags=re.DOTALL)
    return post
