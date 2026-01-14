import re

ICONS = {
    "note": "pen",
    "info": "info",
    "todo": "circle-check",
    "question": "circle-question-mark",
    "help": "circle-question-mark",
    "faq": "circle-question-mark",
    "warning": "circle-alert",
    "caution": "circle-alert",
    "attention": "circle-alert",
    "failure": "x",
    "fail": "x",
    "missing": "x",
    "danger": "zap",
    "error": "zap",
    "bug": "bug",
    "abstract": "clipboard-list",
    "summary": "clipboard-list",
    "tldr": "clipboard-list",
    "tip": "flame",
    "hint": "flame",
    "important": "flame",
    "success": "check",
    "check": "check",
    "done": "check",
    "example": "list",
    "quote": "quote",
    "cite": "quote",
    "others": "book-check",
}


def process_callouts(post):

    def _replacer(match):
        callout_type = match.group("ctype").lower()
        collapse = match.group("collapse")
        title = match.group("title").strip()
        body = re.sub(r"^>\s?", "", match.group("body"), flags=re.MULTILINE)
        return render_callout(callout_type, title, body, collapse)

    callout_pattern = re.compile(
        r"^> \[!\s*(?P<ctype>\w+)\](?P<collapse>[+\-]?)(?P<title>.*?)\n(?P<body>(?:^>.*\n?)*)",
        re.MULTILINE,
    )

    if needs_callout(post.content, callout_pattern):
        post.content = callout_pattern.sub(_replacer, post.content)
        post.content += "\n\n{% include obsidian-callouts.html %}"

    return post


def needs_callout(content, callout_pattern):
    return bool(re.search(callout_pattern, content))


def render_callout(callout_type, title, body, collapse):
    icon = ICONS.get(callout_type, ICONS["others"])
    title = title or callout_type.capitalize()
    tag_map = {"+": "details open", "-": "details"}
    open_tag = tag_map.get(collapse)
    if open_tag:
        content = f"""<{open_tag}>
    <summary class="callout-title"><i class="callout-icon" data-lucide="{icon}"></i>{title}</summary>
    {body}
</details>"""
    else:
        content = f"""<div class="callout-title"><i class="callout-icon" data-lucide="{icon}"></i>{title}</div>
{body}"""

    return (
        f'<div class="callout callout-{callout_type}" markdown="1">\n{content}\n</div>'
    )
