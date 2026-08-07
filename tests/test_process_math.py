import pytest

from src.process_math import process_math


class TestMathSyntax:
    @pytest.mark.parametrize(
        "input_text, expected_fragment",
        [
            ("Value is $x=2$.", r"Value is \\(x=2\\)."),
            (
                "Text $$E=mc^2$$ Text",
                "\n$$E=mc^2$$\n",
            ),
            (
                "$$ x^2 $$ {: #secid1}",
                "$$ x^2 $$\n{: #secid1}",
            ),
        ],
    )
    def test_math_syntax_transformation(self, input_text, expected_fragment, postify):
        post = postify(input_text)
        result = process_math(post)
        assert expected_fragment in result.content


def test_mode_inject_cdn_appends_script(postify, monkeypatch):
    monkeypatch.setattr("src.process_math.MATH_RENDERING_MODE", "inject_cdn")
    post = postify("$1+1$")
    result = process_math(post)

    assert '<script id="MathJax-script"' in result.content


def test_mode_metadata_sets_frontmatter(postify, monkeypatch):
    monkeypatch.setattr("src.process_math.MATH_RENDERING_MODE", "metadata")
    post = postify("$1+1$")
    result = process_math(post)
    assert "<script" not in result.content
    assert result["math"] is True


def test_ignores_posts_without_math(postify):
    post = postify("no math")
    result = process_math(post)

    assert "math" not in result.metadata
    assert "<script" not in result.content


class TestIgnoreInvalidDollars:
    @pytest.mark.parametrize(
        "input", [r"\$50", r"$50", r"$50 and $60", r"$ 50 and$ 60"]
    )
    def test_ignores_escaped_dollars(self, postify, input):
        post = postify(input)
        result = process_math(post)

        assert "<script" not in result.content
        assert result.content == input
