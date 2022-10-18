import os
import statistics
import subprocess
import sys
from _datetime import datetime
from pathlib import Path
from typing import List

import pygit2

from src.Commit import Commit


def git_stats_command(args):
    if len(args) != 1:
        print("Expected one directory as input.")
        return

    path_folder = Path(args[0])
    if not path_folder.is_dir():
        print(f"{path_folder} is not a folder.")
        return

    git_stats(path_folder)


def git_stats(path: Path):
    os.chdir(path)
    repository_path = pygit2.discover_repository(path.as_posix())
    repo = pygit2.Repository(repository_path)
    commits: List[Commit] = []

    for commit in repo.walk(repo.head.target, pygit2.GIT_SORT_TIME):
        commits.append(Commit(date=datetime.fromtimestamp(commit.commit_time), id=commit.id.__str__()))

    size = len(commits)
    for commit_number in range(0, size - 2):
        result = subprocess.run(
            ['git', 'diff', '--shortstat', commits[commit_number].id, commits[commit_number + 1].id],
            stdout=subprocess.PIPE)
        output = [line.split(b' ') for line in result.stdout.replace(b"\n", b"").split(b',')]

        for line in output:
            if len(line) > 2:
                match line[2]:
                    case b'file':
                        commits[commit_number].file_change = int(line[1])
                    case b'files':
                        commits[commit_number].file_change = int(line[1])
                    case b'insertions(+)':
                        commits[commit_number].insertions = int(line[1])
                    case b'deletions(-)':
                        commits[commit_number].deletions = int(line[1])

    list_of_last_commits = commits[0:20]

    print(f"median deletions: {statistics.median([commit.deletions for commit in list_of_last_commits])}")
    print(f"median files change: {statistics.median([commit.file_change for commit in list_of_last_commits])}")
    print(f"median insertions: {statistics.median([commit.insertions for commit in list_of_last_commits])}")
    print(
        f"median number days from last commits: {statistics.median([(commit.date - datetime.now()).days for commit in list_of_last_commits])}")

    print(f"average deletions: {statistics.mean([commit.deletions for commit in list_of_last_commits])}")
    print(f"average files change: {statistics.mean([commit.file_change for commit in list_of_last_commits])}")
    print(f"average insertions: {statistics.mean([commit.insertions for commit in list_of_last_commits])}")
    print(
        f"average number days from last commits: {statistics.mean([(commit.date - datetime.now()).days for commit in list_of_last_commits])}")

    return


if __name__ == "__main__":
    git_stats_command(sys.argv[1:])
