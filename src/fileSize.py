import os
import statistics
import sys
from pathlib import Path
from typing import List


def file_size_command(args):
    if len(args) != 1:
        print("Error: need one argument.")
        return

    path_folder = Path(args[0])
    if not path_folder.is_dir():
        print(f"{path_folder} is not a folder.")
        return

    list_files_size = file_size(path_folder)
    read_stats(list_files_size)


def file_size(path: Path, list_files_size=[]):
    for file in path.iterdir():
        if file.is_dir():
            file_size(file, list_files_size)
        elif file.suffix.upper() == ".JAVA":
            list_files_size.append(os.path.getsize(file))

    return list_files_size


def read_stats(list: List):
    print(f"median size: {statistics.median(list)}")
    print(f"average fsize: {statistics.mean(list)}")
    print(f"std dev size: {statistics.stdev(list)}")
    print(f"min size: {min(list)}")
    print(f"max size: {max(list)}")


if __name__ == "__main__":
    file_size_command(sys.argv[1:])
