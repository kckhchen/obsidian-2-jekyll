import frontmatter
import pytest


@pytest.fixture
def postify():
    def _maker(content, metadata=None):
        return frontmatter.Post(content, **(metadata or {}))

    return _maker
