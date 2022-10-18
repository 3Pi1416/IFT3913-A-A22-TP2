import statistics
import sys
from pathlib import Path


def csec(args):
    if len(args) != 1:
        print("Expected one directory as input.")
        return

    main_folder = Path(args[0])
    if not main_folder.is_dir():
        print(f"{main_folder} is not a folder.")
        return

    file_list = get_file_list(main_folder)
    csec_values = get_csec_values(file_list)
    csec_stats(csec_values)


def get_file_list(folder_path: Path, file_list=[]):
    for file in folder_path.iterdir():
        if file.is_dir():
            get_file_list(file, file_list)
        elif file.suffix.upper() == ".JAVA":
            file_list.append(file)

    return file_list


def get_csec_values(file_list: list):
    csec_values = [0] * len(file_list)

    for i in range(len(file_list)):
        a_file_path = file_list[i]
        a_class_name = a_file_path.stem

        for j in range(i + 1, len(file_list)):
            b_file_path = file_list[j]
            b_class_name = b_file_path.stem

            if mentions(a_file_path, b_class_name) or mentions(b_file_path, a_class_name):
                csec_values[i] += 1
                csec_values[j] += 1

    return csec_values


def mentions(file_path: str, class_name: str):
    with open(file_path) as file:
        for line in file:
            stripped_line = line.strip()
            if stripped_line:
                if stripped_line[:2] == '/*' or stripped_line[:2] == '//' or stripped_line[0] == '*':
                    continue
                elif class_name in line:
                    return True

    return False


def csec_stats(csec_values: list):
    print(f"Median CSEC value: {statistics.median(csec_values)}")
    print(f"Average CSEC value: {statistics.mean(csec_values)}")
    print(f"STD dev of CSEC values: {statistics.stdev(csec_values)}")
    print(f"Min CSEC value: {min(csec_values)}")
    print(f"Max CSEC value: {max(csec_values)}")


if __name__ == "__main__":
    csec(sys.argv[1:])
