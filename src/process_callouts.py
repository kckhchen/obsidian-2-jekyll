import re
from .icons import ICONS


CALLOUT_PATTERN = re.compile(
    r"^> \[!\s*(?P<ctype>\w+)\](?P<collapse>[+\-]?)(?P<title>.*?)\n(?P<body>(?:^>.*\n?)*)",
    re.MULTILINE,
)


def process_callouts(post):
    new_content, count = CALLOUT_PATTERN.subn(_callout_replacer, post.content)

    if count > 0:
        post.content = new_content
        post.content += "\n\n{% include obsidian-callouts.html %}"

    return post


def _callout_replacer(match):
    ctype = match.group("ctype").lower()
    collapse = match.group("collapse")
    title = match.group("title").strip()
    body = re.sub(r"^>\s?", "", match.group("body"), flags=re.MULTILINE)

    body = CALLOUT_PATTERN.sub(_callout_replacer, body)

    return _render_callout(ctype, title, body, collapse)


def _render_callout(callout_type, title, body, collapse):
    icon = ICONS.get(callout_type, ICONS["others"])
    title = title or callout_type.capitalize()
    tag_map = {"+": "details open", "-": "details"}
    open_tag = tag_map.get(collapse)
    if open_tag:
        content = f"""<{open_tag} markdown="1">
<summary class="callout-title"><i class="callout-icon" data-lucide="{icon}"></i><span class="callout-title-text">{title}</span></summary>
{body}</details>"""
    else:
        content = f"""<div class="callout-title"><i class="callout-icon" data-lucide="{icon}"></i><span class="callout-title-text">{title}</span></div>
{body}"""

    return f'<div class="callout callout-{callout_type}" markdown="1">{content}</div>'
