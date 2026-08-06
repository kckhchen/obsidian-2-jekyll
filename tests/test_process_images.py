from pathlib import Path
from unittest.mock import patch

import frontmatter
import pytest

from src.process_images import process_embedded_images


@pytest.fixture
def postify():
    def _maker(content):
        return frontmatter.Post(content)

    return _maker


@pytest.fixture
def img_map():
    return {
        "image.png": Path("/abs/path/to/vault/assets/image.png"),
        "photo.jpg": Path("/abs/path/to/vault/photos/photo.jpg"),
        "graphic.png": Path("/abs/path/to/graphic.png"),
    }


@pytest.fixture
def mock_settings():
    with patch("src.settings.config") as mock:
        mock.IMG_FOLDER = "assets/img"
        yield mock


@pytest.fixture
def mock_shutil():
    with patch("src.process_images.shutil.copy2") as mock_copy:
        yield mock_copy


class TestProcessEmbeddedImages:
    @pytest.mark.parametrize(
        "input_text, expected_output, expected_width_attr",
        [
            pytest.param(
                "![[image.png]]",
                "![]({{ site.baseurl }}{% link assets/img/image.png %})",
                None,
                id="wikilink_basic",
            ),
            pytest.param(
                "![[image.png|300]]",
                '![]({{ site.baseurl }}{% link assets/img/image.png %}){: width="300" }',
                "300",
                id="wikilink_with_width",
            ),
            pytest.param(
                "![](image.png)",
                "![]({{ site.baseurl }}{% link assets/img/image.png %})",
                None,
                id="mdlink_basic",
            ),
            pytest.param(
                "![500](image.png)",
                '![]({{ site.baseurl }}{% link assets/img/image.png %}){: width="500" }',
                "500",
                id="mdlink_with_width",
            ),
            pytest.param(
                "![[IMAGE.PNG]]",
                "![]({{ site.baseurl }}{% link assets/img/IMAGE.PNG %})",
                None,
                id="handles_case_insensitivity",
            ),
        ],
    )
    def test_image_replacement_and_copy(
        self,
        input_text,
        expected_output,
        expected_width_attr,
        postify,
        img_map,
        mock_settings,
        mock_shutil,
    ):
        post = postify(input_text)
        dest_dir = Path("/output/assets")

        result = process_embedded_images(post, img_map, dest_dir)

        assert result.content == expected_output

        assert mock_shutil.called

        assert str(dest_dir) in str(mock_shutil.call_args)

    def test_keeps_tag_if_image_not_in_map(
        self, postify, img_map, mock_settings, capsys
    ):
        post = postify("![[missing_file.png]]")
        dest_dir = Path("/out")

        result = process_embedded_images(post, img_map, dest_dir)

        assert result.content.strip() == "![[missing_file.png]]"

        captured = capsys.readouterr()
        assert "Warning: Image target not found" in captured.out
        assert "missing_file.png" in captured.out

    def test_ignores_non_image_extensions(self, postify, img_map, mock_settings):
        input_text = "![[document.pdf]]"
        post = postify(input_text)
        dest_dir = Path("/out")

        result = process_embedded_images(post, img_map, dest_dir)

        assert result.content == "![](document.pdf)"
        assert "{% link" not in result.content

    def test_handles_spaces_in_filenames(
        self, postify, img_map, mock_settings, mock_shutil
    ):
        img_map["my cool image.png"] = Path("/source/my cool image.png")

        post = postify("![[My Cool Image.png]]")
        dest_dir = Path("/out")

        result = process_embedded_images(post, img_map, dest_dir)

        assert "My Cool Image.png" in result.content
        assert mock_shutil.called


class TestProcessAltText:
    @pytest.mark.parametrize(
        "md, expected_alt, expected_attrs",
        [
            pytest.param("![[image.png]]", "", ""),
            pytest.param("![[image.png|300]]", "", 'width="300"'),
            pytest.param("![[image.png|300x200]]", "", 'width="300" height="200"'),
            pytest.param("![alt text](image.png)", "alt text", ""),
            pytest.param("![alt text|400](image.png)", "alt text", 'width="400"'),
            pytest.param("![400](image.png)", "", 'width="400"'),
            pytest.param("![](image.png)", "", ""),
        ],
    )
    def test_alt_and_size(
        self,
        md,
        expected_alt,
        expected_attrs,
        postify,
        img_map,
        mock_settings,
        mock_shutil,
    ):
        out = process_embedded_images(postify(md), img_map, Path("/tmp")).content
        assert out.startswith(f"![{expected_alt}](")
        assert expected_attrs in out
