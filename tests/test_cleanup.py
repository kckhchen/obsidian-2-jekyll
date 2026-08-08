from unittest.mock import patch

import pytest

from src.cleanup import (
    # _scan_post_images,
    _get_post_images,
    _list_imgs_to_be_removed,
    _list_posts_to_be_removed,
    _remove_files,
    remove_stale_files,
)


@pytest.fixture
def fs_setup(tmp_path):
    post_dir = tmp_path / "posts"
    img_dir = tmp_path / "img"
    post_dir.mkdir()
    img_dir.mkdir()
    return post_dir, img_dir


class TestImageScanning:
    def test_extracts_wiki_and_md_links(self, fs_setup):
        post_dir, _ = fs_setup
        post_path = post_dir / "post.md"
        content = """
        Here is a wikilink: ![]({% link _posts/image1.png %})
        Here is a wikilink with size: ![]({% link _posts/image2.jpg %}){: width="500"}
        Here is a complex md link: ![alt text]({% link _posts/image4.bmp %})
        """
        post_path.write_text(content)
        # post = frontmatter.Post(content)
        images = _get_post_images(post_dir)

        assert set(images) == {"image1.png", "image2.jpg", "image4.bmp"}

    def test_ignores_external_urls(self, fs_setup):
        post_dir, _ = fs_setup
        post_path = post_dir / "post.md"
        content = "![External](https://google.com/logo.png)"
        post_path.write_text(content)
        images = _get_post_images(post_dir)

        assert len(images) == 0

    def test_extracts_filename_from_path(self, fs_setup):
        post_dir, _ = fs_setup
        post_path = post_dir / "post.md"
        content = "![]({% link _posts/photo.jpg %})"
        post_path.write_text(content)
        images = _get_post_images(post_dir)

        assert "photo.jpg" in images


class TestStaleListGeneration:
    def test_list_posts_to_be_removed(self, fs_setup):
        post_dir, _ = fs_setup

        (post_dir / "2023-01-01-kept.md").write_text(
            "---\ngenerator: obsidian-2-jekyll\n---"
        )
        (post_dir / "2023-01-01-stale.md").write_text(
            "---\ngenerator: obsidian-2-jekyll\n---"
        )
        (post_dir / "2023-01-01-notmd.txt").write_text(
            "---\ngenerator: obsidian-2-jekyll\n---"
        )
        (post_dir / "2023-01-01-notmanaged.md").write_text("---\n---")

        current_posts = {"2023-01-01-kept.md"}

        to_remove = _list_posts_to_be_removed(post_dir, current_posts)

        filenames = [p.name for p in to_remove]
        assert "2023-01-01-stale.md" in filenames
        assert "2023-01-01-kept.md" not in filenames
        assert "2023-01-01-notmd.txt" not in filenames
        assert "2023-01-01-notmanaged.md" not in filenames

    def test_list_imgs_to_be_removed(self, fs_setup):
        _, img_dir = fs_setup

        (img_dir / "used.png").touch()
        (img_dir / "unused.jpg").touch()
        (img_dir / "not_an_image.txt").touch()

        all_post_images = {"used.png"}

        to_remove = _list_imgs_to_be_removed(img_dir, all_post_images)

        filenames = [p.name for p in to_remove]
        assert "unused.jpg" in filenames
        assert "used.png" not in filenames
        assert "not_an_image.txt" not in filenames


class TestDeletionSafety:
    def test_remove_files_aborts_on_no(self, fs_setup):
        post_dir, _ = fs_setup
        stale_file = post_dir / "delete_me.md"
        stale_file.touch()

        with patch("builtins.input", return_value="n"):
            _remove_files([stale_file])

        assert stale_file.exists()

    def test_remove_files_proceeds_on_yes(self, fs_setup):
        post_dir, _ = fs_setup
        stale_file = post_dir / "delete_me.md"
        stale_file.touch()

        with patch("builtins.input", return_value="y"):
            _remove_files([stale_file])

        assert not stale_file.exists()


class TestFullFlow:
    def test_remove_stale_files_integration(self, fs_setup, mocker):
        post_dir, img_dir = fs_setup

        valid_dest = post_dir / "2023-01-01-valid.md"
        stale_dest = post_dir / "2023-01-01-stale.md"
        used_img = img_dir / "used_image.png"
        stale_img = img_dir / "stale_image.jpg"

        valid_dest.write_text(
            "---\ngenerator: obsidian-2-jekyll\n---\n![[used_image.png]]"
        )
        stale_dest.write_text("---\ngenerator: obsidian-2-jekyll\n---")
        used_img.touch()
        stale_img.touch()

        valid_files = {"valid": {"dest_path": valid_dest}}

        with patch("builtins.input", return_value="y"):
            mock_get_post_images = mocker.patch("src.cleanup._get_post_images")
            mock_get_post_images.return_value = {"used_image.png"}
            remove_stale_files(valid_files, post_dir, img_dir)

        assert valid_dest.exists()
        assert used_img.exists()

        assert not stale_dest.exists()
        assert not stale_img.exists()
