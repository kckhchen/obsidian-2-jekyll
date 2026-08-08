import frontmatter
import pytest

from src.callout_styles import CALLOUT_CSS
from src.fs_ops import copy_images, ensure_css_exists, setup_dir


@pytest.fixture
def css_mock(tmp_path, monkeypatch):
    monkeypatch.setattr("src.fs_ops.INCLUDES_FOLDER", "_includes")
    monkeypatch.setattr("src.fs_ops.JEKYLL_DIR", str(tmp_path))


def test_setup_dir_creates_folders(tmp_path, capsys):
    post_dir = tmp_path / "out/posts"
    img_dir = tmp_path / "out/assets/img"

    assert not post_dir.exists()

    setup_dir([post_dir, img_dir], dry=False)

    assert post_dir.exists()
    assert img_dir.exists()

    captured = capsys.readouterr()
    assert "Destination folder not found, creating" in captured.out


def test_setup_dir_respects_dry_run(tmp_path):
    post_dir = tmp_path / "posts"
    img_dir = tmp_path / "img"

    setup_dir([post_dir, img_dir], dry=True)

    assert not post_dir.exists()


def test_ensure_css_exists_writes_file(css_mock, tmp_path):
    css_name = "test-callouts.css"
    expected_path = tmp_path / "_includes" / css_name

    ensure_css_exists(css_name, dry=False)

    assert expected_path.exists()

    assert expected_path.read_text(encoding="utf-8") == CALLOUT_CSS


def test_ensure_css_skips_if_already_exists(tmp_path, css_mock, capsys):
    css_name = "existing.css"
    includes = tmp_path / "_includes"
    includes.mkdir()

    (includes / css_name).write_text("OLD CONTENT", encoding="utf-8")

    ensure_css_exists(css_name, dry=False)

    assert (includes / css_name).read_text(encoding="utf-8") == "OLD CONTENT"

    captured = capsys.readouterr()
    assert "Creating default callout CSS" not in captured.out


def test_external_image_url_does_not_crash(tmp_path):
    post = frontmatter.Post("![](https://cdn.example.com/x.png)")
    copy_images(post, {}, tmp_path)
