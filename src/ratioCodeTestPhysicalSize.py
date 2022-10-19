import os
import sys
from pathlib import Path


def calculate_test_to_code_size_ratio(args):
    if len(args) != 2:
        print("Expected two directories as arguments.")
        return

    main = Path(args[0])
    if not main.is_dir():
        print(f"{main} is not a folder.")
        return

    test = Path(args[1])
    if not test.is_dir():
        print(f"{test} is not a folder.")

    main_folder = args[0]
    test_folder = args[1]
    size_test = 0
    size_code = 0

    for path, directory, files in os.walk(main_folder):
        for f in files:
            file_path = os.path.join(path, f)
            size_code += os.path.getsize(file_path)

    for path, directory, files in os.walk(test_folder):
        for f in files:
            file_path = os.path.join(path, f)
            size_test += os.path.getsize(file_path)

    print(size_code / size_test)


if __name__ == "__main__":
    calculate_test_to_code_size_ratio(sys.argv[1:])