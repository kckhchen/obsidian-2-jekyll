import frontmatter
import pytest

from src.process_math import process_math


@pytest.fixture
def postify():
    def _maker(content, metadata=None):
        return frontmatter.Post(content, **(metadata or {}))

    return _maker


class TestProcessMath:
    @pytest.mark.parametrize(
        "input_text, expected_fragment",
        [
            pytest.param(
                "Value is $x=2$.", r"Value is \\(x=2\\).", id="converts_inline_math"
            ),
            pytest.param(
                "Text $$E=mc^2$$ Text",
                "\n$$E=mc^2$$\n",
                id="formats_block_math_with_newlines",
            ),
            pytest.param(
                "$$ x^2 $$ {: #secid1}",
                "$$ x^2 $$\n{: #secid1}",
                id="moves_block_id_to_newline",
            ),
        ],
    )
    def test_math_syntax_transformation(
        self, input_text, expected_fragment, postify, monkeypatch
    ):
        monkeypatch.setattr("src.process_math.MATH_RENDERING_MODE", "inject_cdn")
        post = postify(input_text)
        result = process_math(post)
        assert expected_fragment in result.content

    def test_mode_inject_cdn_appends_script(self, postify, monkeypatch):
        monkeypatch.setattr("src.process_math.MATH_RENDERING_MODE", "inject_cdn")
        post = postify("Here is some math $1+1$")
        result = process_math(post)

        assert '<script id="MathJax-script"' in result.content
        assert "mathjax@4" in result.content

    def test_mode_metadata_sets_frontmatter(self, postify, monkeypatch):
        monkeypatch.setattr("src.process_math.MATH_RENDERING_MODE", "metadata")

        post = postify("Here is some math $1+1$")
        result = process_math(post)

        assert "<script" not in result.content
        assert result["math"] is True

    def test_ignores_posts_without_math(self, postify):
        original_content = "Just plain text with no numbers."
        post = postify(original_content)

        result = process_math(post)

        assert result.content == original_content
        assert "math" not in result.metadata
        assert "<script" not in result.content

    def test_ignores_escaped_dollars(self, postify):
        text = r"This costs \$50 dollars."
        post = postify(text)

        result = process_math(post)

        assert "<script" not in result.content
        assert result.content == text
