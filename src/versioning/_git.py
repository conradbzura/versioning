import git

from src.versioning._version import parser


@parser("git")
def parse() -> str:
    """Parses the current git repository to generate a version string.

    Returns:
        A version string based on the latest tag, commit hash, and uncommitted
        changes.

    Raises:
        RuntimeError: If the repository is empty.
    """
    repo = git.Repo()
    if repo.bare:
        raise RuntimeError(
            f"The repo at '{repo.working_dir}' cannot be empty!"
        )
    head_commit = repo.head.commit
    try:
        tag = repo.tags[-1]
    except IndexError:
        tag_name = "0"
        tag_commit = None
    else:
        tag_name = tag.name
        tag_commit = tag.commit
    public, *local = tag_name.split("+")
    if head_commit != tag_commit:
        commit_label = head_commit.hexsha
        local.append(commit_label)
    dirty = repo.index.diff(None) or repo.untracked_files
    if dirty:
        local.append("dirty")
    local = ".".join(local)
    return f"{public}+{local}" if local else public
