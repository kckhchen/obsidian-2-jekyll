import re


def process_callouts(post):

    def _replacer(match):
        callout_type = match.group(1).lower()
        collapse = match.group(2)
        title = match.group(3).strip()
        body = re.sub(r"^>\s?", "", match.group(4), flags=re.MULTILINE)
        return render_callout(callout_type, title, body, collapse)

    callout_pattern = re.compile(
        r"^> \[!\s*(\w+)\]([+\-]?)(.*?)\n((?:^>.*\n?)*)", re.MULTILINE
    )

    if needs_callout(post.content, callout_pattern):
        post.content = callout_pattern.sub(_replacer, post.content)
        post.content += "\n\n{% include obsidian-callouts.html %}"

    return post


def needs_callout(content, callout_pattern):
    return bool(re.search(callout_pattern, content))


def render_callout(callout_type, title, body, collapse):
    title = title or callout_type.capitalize()
    tag_map = {"+": "details open", "-": "details"}
    open_tag = tag_map.get(collapse)
    if open_tag:
        content = f"""<{open_tag}>
    <summary class="callout-title">{title}</summary>
    {body}
</details>"""
    else:
        content = f"""<div class="callout-title">{title}</div>
{body}"""

    return (
        f'<div class="callout callout-{callout_type}" markdown="1">\n{content}\n</div>'
    )
