import pytest
import os
import time
from pathlib import Path
from unittest.mock import patch, Mock, call
from src.processor_core import pre_process, process_posts, _should_proceed, _iter_files


def test_should_proceed_logic(tmp_path):
    src = tmp_path / "source.md"
    dest = tmp_path / "dest.md"
    src.touch()

    assert _should_proceed(src, dest, force=False) == "Creating"

    dest.touch()

    os.utime(src, (100, 100))
    os.utime(dest, (200, 200))
    assert _should_proceed(src, dest, force=False) is False

    assert _should_proceed(src, dest, force=True) == "Force Updating"

    os.utime(src, (300, 300))
    assert _should_proceed(src, dest, force=False) == "Updating"


@pytest.fixture
def mock_files_map():
    return {
        "Post A": {"source_path": Path("a.md"), "dest_path": Path("out/a.md")},
        "Post B": {"source_path": Path("b.md"), "dest_path": Path("out/b.md")},
    }


def test_iter_files_yields_all_by_default(mock_files_map):

    with patch("src.processor_core.frontmatter.load", return_value="dummy_post"):
        results = list(_iter_files(mock_files_map, only_file=None))

    assert len(results) == 2

    assert results[0][0] == Path("a.md")


def test_iter_files_filters_single_file(mock_files_map):
    with patch("src.processor_core.frontmatter.load", return_value="dummy_post"):
        results = list(_iter_files(mock_files_map, only_file="Post B.md"))

    assert len(results) == 1
    assert results[0][0] == Path("b.md")


def test_iter_files_raises_on_missing_file(mock_files_map):
    with pytest.raises(ValueError) as exc:
        list(_iter_files(mock_files_map, only_file="Non Existent"))
    assert "Cannot find 'Non Existent'" in str(exc.value)


@patch("src.processor_core._iter_files")
@patch("src.processor_core._should_proceed")
@patch("src.processor_core._process_single_post")
@patch("src.processor_core.frontmatter.dump")
def test_process_posts_flow(mock_dump, mock_process, mock_proceed, mock_iter, capsys):

    src1, dest1 = Path("s1"), Path("d1")
    src2, dest2 = Path("s2"), Path("d2")
    src3, dest3 = Path("s3"), Path("d3")

    mock_iter.return_value = [
        (src1, dest1, "post1"),
        (src2, dest2, "post2"),
        (src3, dest3, "post3"),
    ]

    mock_proceed.side_effect = [False, "Creating", "Creating"]

    process_posts({}, {}, Path("."), False, "post", False)

    assert mock_process.call_count == 2

    assert mock_dump.call_count == 2

    captured = capsys.readouterr()
    assert "Skipped 1 unchanged files" in captured.out
    assert "Creating: s2" in captured.out


def test_process_posts_handles_errors_gracefully(capsys):
    with patch("src.processor_core._iter_files", side_effect=FileNotFoundError("Boom")):
        process_posts({}, {}, Path("."), False, "post", False)

    captured = capsys.readouterr()
    assert "Boom" in captured.out


@patch("src.processor_core.build_img_map")
@patch("src.processor_core.ensure_css_exists")
@patch("src.processor_core.setup_dir")
@patch("src.processor_core.announce_paths")
def test_pre_process_calls_helpers(mock_announce, mock_setup, mock_css, mock_img_map):
    mock_img_map.return_value = {"img": "path"}

    result = pre_process("vault", "post", "img", dry=False)

    mock_announce.assert_called_with("vault", "post", False)
    mock_setup.assert_called_with("post", "img", False)
    mock_css.assert_called_with("obsidian-callouts.html", False)
    mock_img_map.assert_called_with("vault")

    assert result == {"img": "path"}
