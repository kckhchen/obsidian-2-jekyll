import pytest

from src.processor_core import process_posts
from src.utils import get_valid_files


@pytest.fixture
def mock_fs(tmp_path):
    post_dir = tmp_path / "_posts"
    img_dir = tmp_path / "assets/images/obsidian"
    vault_dir = tmp_path / "vault"
    post_dir.mkdir()
    img_dir.mkdir(parents=True, exist_ok=True)
    vault_dir.mkdir()
    return vault_dir, post_dir, img_dir


def test_invariant(mock_fs):
    vault_dir, post_dir, _ = mock_fs
    input_post = vault_dir / "input.md"
    content = "---\nshare: true\ndate: 2013-01-01\n---\nTitle\n=====\nContent, $299, $499, $ 100|200$, `x == y`, `$5`, ```markdown\n> [!note] Callout Title\n> Callout Content\n```"
    input_post.write_text(content)
    valid_files = get_valid_files(vault_dir, post_dir)
    process_posts(valid_files, dry=False, layout=None, force=False)
    output = post_dir / "2013-01-01-input.md"
    out = output.read_text()
    should_exist = [
        "$299",
        "$499",
        "Title\n=====",
        "$ 100|200$",
        "`x == y`",
        "`$5`",
        "> [!note] Callout Title",
        "> Callout Content",
    ]

    assert output.exists()
    for text in should_exist:
        assert text in out
