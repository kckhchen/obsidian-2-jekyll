import pytest
import frontmatter
from unittest.mock import patch, Mock
from pathlib import Path
from datetime import datetime
from src.utils import (
    get_creation_time,
    slugify,
    validate_configs,
    shield_content,
    unshield,
    get_valid_files,
    _get_dest_fpath,
)


@pytest.fixture
def mock_config():
    m = Mock()
    m.MATH_RENDERING_MODE = "inject_cdn"
    return m


class TestPureHelpers:

    @pytest.mark.parametrize(
        "name, expected",
        [
            ("My New Post", "my-new-post"),
            ("Hello   World", "hello-world"),
            ("C++ Programming", "c-programming"),
            ("File_Name_With_Underscores", "file_name_with_underscores"),
            ("---Trim Dashes---", "trim-dashes"),
        ],
    )
    def test_slugify(self, name, expected):
        assert slugify(name) == expected

    def test_get_creation_time(self):

        with patch("pathlib.Path.stat") as mock_stat:

            mock_stat.return_value.st_mtime = 1672531200.0

            mock_stat.return_value.st_birthtime = 1672531200.0

            result = get_creation_time("dummy_path")
            assert result == "2023-01-01"


class TestValidation:

    def test_validate_configs_success(self, tmp_path, mock_config):

        validate_configs(tmp_path, mock_config)

    def test_validate_configs_missing_vault(self, mock_config):
        missing_path = Path("/non/existent/path")
        with pytest.raises(FileNotFoundError):
            validate_configs(missing_path, mock_config)

    def test_validate_configs_invalid_mode(self, tmp_path, mock_config):
        mock_config.MATH_RENDERING_MODE = "bad_mode"
        with pytest.raises(ValueError) as exc:
            validate_configs(tmp_path, mock_config)
        assert "Invalid MATH_RENDERING_MODE" in str(exc.value)


class TestShielding:

    def test_shield_code_blocks(self, postify):
        content = "Text\n```python\nprint(1)\n```\nMore Text"
        post = postify(content)

        post, stash = shield_content(post, mode="code")

        assert "&&CODE_0&&" in post.content
        assert "print(1)" not in post.content

        assert stash["&&CODE_0&&"] == "```python\nprint(1)\n```"

    def test_shield_urls(self, postify):
        content = "Check https://google.com now."
        post = postify(content)

        post, stash = shield_content(post, mode="url")

        assert "Check &&URL_0&& now." == post.content
        assert stash["&&URL_0&&"] == "https://google.com"

    def test_unshield_restores_content(self, postify):
        post = postify("Check &&URL_0&&.")
        stash = {"&&URL_0&&": "https://google.com"}

        unshield(post, stash)

        assert post.content == "Check https://google.com."

    def test_unshield_with_convert_func(self, postify):

        post = postify("Code: &&CODE_0&&")
        stash = {"&&CODE_0&&": "my_code"}

        def converter(text):
            return text.upper()

        unshield(post, stash, convert_func=converter)

        assert post.content == "Code: MY_CODE"


class TestFileScanning:
    """
    Uses 'tmp_path' to create a real mini-vault to test 'get_valid_files'.
    This is much more reliable than mocking os.walk/rglob.
    """

    @pytest.fixture
    def mini_vault(self, tmp_path):

        vault = tmp_path / "Vault"
        vault.mkdir()

        p1 = vault / "post1.md"
        p1.write_text("---\nshare: true\ntitle: Post 1\n---\nContent", encoding="utf-8")

        p2 = vault / "private.md"
        p2.write_text(
            "---\nshare: false\ntitle: Secret\n---\nContent", encoding="utf-8"
        )

        p3 = vault / "bad.md"
        p3.write_text("Just text", encoding="utf-8")

        p4 = vault / "image.png"
        p4.write_text("binary", encoding="utf-8")

        return vault

    def test_get_valid_files_filters_correctly(self, mini_vault, tmp_path):
        post_dir = tmp_path / "output"

        with patch("src.utils._get_dest_fpath", return_value=Path("out/post1.md")):
            results = get_valid_files(mini_vault, post_dir)

        assert "post1" in results
        assert "private" not in results
        assert "bad" not in results
        assert "image" not in results

        assert results["post1"]["source_path"] == mini_vault / "post1.md"


class TestDestPathLogic:

    def test_uses_date_from_frontmatter(self, postify):
        post = postify("cnt", metadata={"date": "2025-05-05"})
        source_path = Path("My Post.md")
        post_dir = Path("out")

        result = _get_dest_fpath(post, source_path, post_dir)

        assert result.name == "2025-05-05-my-post.md"

    def test_falls_back_to_creation_time_if_no_date(self, postify):
        post = postify("cnt")
        source_path = Path("My Post.md")
        post_dir = Path("out")

        with patch("src.utils.get_creation_time", return_value="2020-01-01"):
            result = _get_dest_fpath(post, source_path, post_dir)

        assert result.name == "2020-01-01-my-post.md"

    def test_cleans_existing_date_prefix_from_filename(self, postify):

        post = postify("cnt", metadata={"date": "2025-05-05"})

        source_path = Path("2022-01-01 My Post.md")
        post_dir = Path("out")

        result = _get_dest_fpath(post, source_path, post_dir)

        assert result.name == "2025-05-05-my-post.md"
