import re
from . import settings


def process_math(post):
    if needs_math(post.content):
        mathjax_script = '<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@4/tex-mml-chtml.js"></script>'
        inline_math_pattern = r"(?<!\\|\$)\$([^$]+?)(?<!\\)\$(?!\$)"
        post.content = re.sub(inline_math_pattern, r"\\\\(\1\\\\)", post.content)
        post.content = re.sub(
            r"(\$\$.*?\$\$)", r"\n\1\n", post.content, flags=re.DOTALL
        )

        if settings.config.MATH_RENDERING_MODE == "inject_cdn":
            post.content += f"\n\n{mathjax_script}"
        elif settings.config.MATH_RENDERING_MODE == "metadata":
            post["math"] = post.get("math") or True
        else:
            print(
                'Math blocks detected but no rendering mode is selected. Please either set MATH_RENDERING_MODE = "inject_cdn" or "metadata".\n'
            )

        post = fix_math_id(post)

    return post


def needs_math(content):
    has_block_math = bool(re.search(r"\$\$.*?\$\$", content, flags=re.DOTALL))
    has_inline_math = bool(re.search(r"(?<!\\)\$[^ \t\n\$].*?\$", content))

    return has_block_math or has_inline_math


def fix_math_id(post):

    pattern = r"\$\$[\s\n]+({: #secid.+})"
    post.content = re.sub(pattern, r"$$\n\1", post.content)

    return post
