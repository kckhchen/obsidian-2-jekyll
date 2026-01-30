import pytest
from pathlib import Path
from unittest.mock import patch, Mock
from src.fs_ops import build_img_map, setup_dir, ensure_css_exists, announce_paths


from src.templates import CALLOUT_CSS


def test_build_img_map_finds_nested_images(tmp_path):
    """
    /vault
      /images
         img1.png
         IMG2.JPG
      /notes
         note.md
    """
    vault = tmp_path / "vault"
    images = vault / "images"
    notes = vault / "notes"
    images.mkdir(parents=True)
    notes.mkdir(parents=True)

    (images / "img1.png").touch()
    (images / "IMG2.JPG").touch()
    (images / "random.txt").touch()
    (notes / "note.md").touch()

    result = build_img_map(vault)

    assert "img1.png" in result
    assert "img2.jpg" in result

    assert "note.md" not in result
    assert "random.txt" not in result

    assert result["img1.png"] == images / "img1.png"


def test_setup_dir_creates_folders(tmp_path, capsys):

    post_dir = tmp_path / "out/posts"
    img_dir = tmp_path / "out/assets/img"

    assert not post_dir.exists()

    setup_dir(post_dir, img_dir, dry=False)

    assert post_dir.exists()
    assert img_dir.exists()

    captured = capsys.readouterr()
    assert "Destination folder not found, creating" in captured.out


def test_setup_dir_respects_dry_run(tmp_path):
    post_dir = tmp_path / "posts"
    img_dir = tmp_path / "img"

    setup_dir(post_dir, img_dir, dry=True)

    assert not post_dir.exists()


@pytest.fixture
def mock_settings_for_css(tmp_path):
    with patch("src.settings.config") as mock_config:

        mock_config.JEKYLL_DIR = str(tmp_path)
        mock_config.INCLUDES_FOLDER = "_includes"
        yield mock_config


def test_ensure_css_exists_writes_file(tmp_path, mock_settings_for_css):
    css_name = "test-callouts.css"
    expected_path = tmp_path / "_includes" / css_name

    ensure_css_exists(css_name, dry=False)

    assert expected_path.exists()

    assert expected_path.read_text(encoding="utf-8") == CALLOUT_CSS


def test_ensure_css_skips_if_already_exists(tmp_path, mock_settings_for_css, capsys):
    css_name = "existing.css"
    includes = tmp_path / "_includes"
    includes.mkdir()

    (includes / css_name).write_text("OLD CONTENT", encoding="utf-8")

    ensure_css_exists(css_name, dry=False)

    assert (includes / css_name).read_text(encoding="utf-8") == "OLD CONTENT"

    captured = capsys.readouterr()
    assert "Creating default callout CSS" not in captured.out


def test_announce_paths_dry_mode(capsys):
    announce_paths("src", "dest", dry=True)
    captured = capsys.readouterr()
    assert "DRY RUN MODE" in captured.out
    assert "src" in captured.out


def test_announce_paths_normal_mode(capsys):
    announce_paths("src", "dest", dry=False)
    captured = capsys.readouterr()
    assert "DRY RUN MODE" not in captured.out
    assert "Start processing posts" in captured.out
