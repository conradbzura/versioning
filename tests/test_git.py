from unittest import mock

import pytest

from versioning._git import parse


@pytest.fixture
def mock_repo():
    with mock.patch(
        "src.versioning._git.git.Repo", autospec=True
    ) as mock_repo:
        yield mock_repo


def test_parse_clean_repo(mock_repo):
    repo_instance = mock_repo.return_value
    repo_instance.bare = False
    repo_instance.head.commit.hexsha = "abc123"
    repo_instance.tags = []
    repo_instance.index.diff.return_value = []
    repo_instance.untracked_files = []

    result = parse()
    assert result == "0+abc123"


def test_parse_dirty_repo(mock_repo):
    repo_instance = mock_repo.return_value
    repo_instance.bare = False
    repo_instance.head.commit.hexsha = "abc123"
    repo_instance.tags = []
    repo_instance.index.diff.return_value = ["file1"]
    repo_instance.untracked_files = []

    result = parse()
    assert result == "0+abc123.dirty"


def test_parse_with_tag(mock_repo):
    repo_instance = mock_repo.return_value
    repo_instance.bare = False
    mock_commit = mock.Mock(hexsha="abc123")
    repo_instance.head.commit = mock_commit
    mock_tag = mock.Mock()
    mock_tag.name = "1.0.0"
    mock_tag.commit = mock_commit
    repo_instance.tags = [mock_tag]
    repo_instance.index.diff.return_value = []
    repo_instance.untracked_files = []

    result = parse()
    assert result == "1.0.0"


def test_parse_with_tag_and_local_changes(mock_repo):
    repo_instance = mock_repo.return_value
    repo_instance.bare = False
    repo_instance.head.commit.hexsha = "def456"
    tag_mock = mock.Mock()
    tag_mock.name = "1.0.0"
    tag_mock.commit.hexsha = "abc123"
    repo_instance.tags = [tag_mock]
    repo_instance.index.diff.return_value = []
    repo_instance.untracked_files = []

    result = parse()
    assert result == "1.0.0+def456"
