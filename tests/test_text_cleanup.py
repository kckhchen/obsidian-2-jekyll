import pytest
import frontmatter
from src.text_cleanup import (
    text_cleanup,
    process_h1,
    strip_comments,
    process_highlights,
    ensure_table_spacing,
)


class TestTextCleanup:

    def test_h1_moves_to_title_metadata(self, postify):

        content = "# My Great Post\n\nBody text here."
        post = postify(content)

        result = process_h1(post)

        assert result["title"] == "My Great Post"
        assert result.content == "Body text here."

    def test_h1_preserves_existing_metadata_title(self, postify):

        content = "# H1 Title\n\nBody."

        post = postify(content, metadata={"title": "Original Metadata Title"})

        result = process_h1(post)

        assert result["title"] == "Original Metadata Title"
        assert result.content == "Body."

    def test_h1_sets_default_layout(self, postify):

        post = postify("# Title")
        process_h1(post)
        assert post["layout"] == "post"

    @pytest.mark.parametrize(
        "input_text, expected_content",
        [
            pytest.param(
                "Text %% hidden comment %% Text", "Text  Text", id="inline_comment"
            ),
            pytest.param(
                "Start\n%% multi\nline\ncomment %%\nEnd",
                "Start\n\nEnd",
                id="multiline_comment",
            ),
        ],
    )
    def test_strip_comments(self, input_text, expected_content, postify):
        post = postify(input_text)
        result = strip_comments(post)
        assert result.content.strip() == expected_content.strip()

    def test_process_highlights(self, postify):
        post = postify("This is ==highlighted== text.")
        result = process_highlights(post)
        assert result.content == "This is <mark>highlighted</mark> text."

    def test_ensure_table_spacing_fixes_cramped_tables(self, postify):

        bad_markdown = "Preceding text\n| Header | Col |\n|---|---|\n| Val | Val |"

        post = postify(bad_markdown)
        result = ensure_table_spacing(post)

        assert "Preceding text\n\n| Header |" in result.content

    def test_ensure_table_spacing_ignores_correct_tables(self, postify):

        good_markdown = "Preceding text\n\n| Header | Col |\n|---|---|"

        post = postify(good_markdown)
        result = ensure_table_spacing(post)

        assert result.content == good_markdown

    def test_text_cleanup_orchestrator(self, postify):

        raw_text = """# Main Title

%% secret %%
Intro text.
==Important== point.
Table follows:
| A | B |
|---|---|
"""
        post = postify(raw_text)

        result = text_cleanup(post)

        assert result["title"] == "Main Title"
        assert "# Main Title" not in result.content
        assert "%% secret %%" not in result.content
        assert "<mark>Important</mark>" in result.content
        assert "follows:\n\n| A |" in result.content
