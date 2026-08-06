import re

from config import MATH_RENDERING_MODE

from .patterns import BLOCK_MATH_PATTERN, INLINE_MATH_PATTERN, MATH_ID_PATTERN


def process_math(post):
    if _needs_math(post.content):
        mathjax_script = '<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@4/tex-mml-chtml.js"></script>'
        post.content = re.sub(INLINE_MATH_PATTERN, r"\\\\(\1\\\\)", post.content)
        post.content = re.sub(
            BLOCK_MATH_PATTERN, r"\n\1\n", post.content, flags=re.DOTALL
        )

        if MATH_RENDERING_MODE == "inject_cdn":
            post.content += f"\n\n{mathjax_script}"
        elif MATH_RENDERING_MODE == "metadata":
            post["math"] = post.get("math") or True

        post = _fix_math_id(post)

    return post


def _needs_math(content):
    has_block_math = bool(re.search(BLOCK_MATH_PATTERN, content, flags=re.DOTALL))
    has_inline_math = bool(re.search(INLINE_MATH_PATTERN, content))

    return has_block_math or has_inline_math


def _fix_math_id(post):
    post.content = re.sub(MATH_ID_PATTERN, r"$$\n\1", post.content)

    return post
