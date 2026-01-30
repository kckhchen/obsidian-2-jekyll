import pytest
from unittest.mock import patch
from src.process_callouts import process_callouts


@pytest.fixture(autouse=True)
def mock_icons():
    with patch("src.process_callouts.ICONS", {"note": "pen", "others": "star"}) as m:
        yield m


class TestProcessCallouts:

    @pytest.mark.parametrize(
        "input_text, expected_fragment",
        [
            pytest.param(
                "> [!note] My Title\n> My content",
                '<div class="callout callout-note" markdown="1">',
                id="basic_callout_structure",
            ),
            pytest.param(
                "> [!note] My Title\n> My content",
                '<span class="callout-title-text">My Title</span>',
                id="renders_custom_title",
            ),
            pytest.param(
                "> [!note]\n> Content",
                '<span class="callout-title-text">Note</span>',
                id="defaults_title_if_missing",
            ),
            pytest.param(
                "> [!unknown]\n> Content",
                'data-lucide="star"',
                id="uses_fallback_icon_for_unknown_types",
            ),
            pytest.param(
                "> [!note]+\n> Content",
                '<details open markdown="1">',
                id="renders_open_details_for_plus",
            ),
            pytest.param(
                "> [!note]-\n> Content",
                '<details markdown="1">',
                id="renders_closed_details_for_minus",
            ),
        ],
    )
    def test_callout_rendering(self, input_text, expected_fragment, postify):
        post = postify(input_text)
        result = process_callouts(post)
        assert expected_fragment in result.content

    def test_injects_liquid_include_only_when_callout_exists(self, postify):
        post_with = postify("> [!note] Test\n> body")
        assert (
            "{% include obsidian-callouts.html %}"
            in process_callouts(post_with).content
        )

        post_without = postify("Just normal text.")
        assert (
            "{% include obsidian-callouts.html %}"
            not in process_callouts(post_without).content
        )

    def test_handles_nested_callouts(self, postify):
        """Verifies recursion works for nested blockquotes."""
        text = """
> [!note] Parent
> Parent Body
> > [!note] Child
> > Child Body
        """
        post = postify(text.strip())
        result = process_callouts(post).content

        assert result.count("callout-note") == 2
        assert "Parent Body" in result
        assert "Child Body" in result

    def test_handles_multiline_body_correctly(self, postify):
        text = "> [!note] Title\n> Line 1\n> Line 2\n"
        post = postify(text)
        result = process_callouts(post).content
        assert "Line 1\nLine 2" in result
