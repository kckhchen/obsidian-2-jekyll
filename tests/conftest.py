import pytest
import frontmatter


@pytest.fixture
def postify():
    def _maker(content):
        return frontmatter.Post(content)

    return _maker
