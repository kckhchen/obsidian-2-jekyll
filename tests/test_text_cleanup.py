from src.text_cleanup import (
    _ensure_table_spacing,
    _process_h1,
    text_cleanup,
)


class TestTextCleanup:
    def test_h1_preserves_existing_metadata_title(self, postify):
        content = "# H1 Title"
        post = postify(content, metadata={"title": "Original Metadata Title"})
        result = _process_h1(post)
        assert result["title"] == "Original Metadata Title"

    def test_ensure_table_spacing_fixes_cramped_tables(self, postify):
        bad_markdown = "Preceding text\n| Header | Col |\n|---|---|\n| Val | Val |"
        post = postify(bad_markdown)
        result = _ensure_table_spacing(post)
        assert "Preceding text\n\n| Header |" in result.content

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
