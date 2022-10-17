import sys
from pathlib import Path


def ratio_test_java_files_command(args):
    if len(args) != 2:
        print("Error: need two argument.")
        return

    path_folder = Path(args[0])
    if not path_folder.is_dir():
        print(f"{path_folder} is not a folder.")
        return

    path_folder_test = Path(args[1])
    if not path_folder.is_dir():
        print(f"{path_folder_test} is not a folder.")
        return

    number_of_test_files = calculate_number_of_test_file(path_folder_test)
    public_classes, private_classes, interface, abstract_classes, other = calculate_number_of_java_file(path_folder)

    print(f"Nombre de fichier test:{number_of_test_files}")
    print(f"Nombre de public class:{public_classes}")
    print(f"Nombre de private class:{private_classes}")
    print(f"Nombre de interface:{interface}")
    print(f"Nombre de abstract class:{abstract_classes}")
    print(f"Nombre de autre( example enum) :{other}")


def calculate_number_of_test_file(path: Path):
    number_of_test_files = 0
    for file in path.iterdir():
        if file.is_dir():
            number_of_test_files = number_of_test_files + calculate_number_of_test_file(file)
        elif file.suffix.upper() == ".JAVA":
            number_of_test_files = number_of_test_files + 1

    return number_of_test_files


def calculate_number_of_java_file(path: Path):
    public_classes = 0
    private_classes = 0
    interface = 0
    abstract_classes = 0
    other = 0
    for file in path.iterdir():
        if file.is_dir():
            add_classes, add_private_classes, add_interface, add_abstract_classes, add_other = calculate_number_of_java_file(
                file)
            public_classes = public_classes + add_classes
            interface = interface + add_interface
            abstract_classes = abstract_classes + add_abstract_classes
            private_classes = private_classes + add_private_classes
            other = other + add_other

        elif file.suffix.upper() == ".JAVA":
            match find_file_type(file):
                case "class":
                    public_classes = public_classes + 1
                case "interface":
                    interface = interface + 1
                case "abstract":
                    abstract_classes = abstract_classes + 1
                case "private":
                    private_classes = private_classes + 1
                case _:
                    other = other + 1

    return public_classes, private_classes, interface, abstract_classes, other


def find_file_type(java_file):
    with open(java_file) as open_file:
        for line in open_file:
            words = []
            for word in line.split(" "):
                if word:
                    words.append(word)

            if words[0] == "public":
                return words[1]
            if words[0] == "class":
                return "private"

    return "other"


if __name__ == "__main__":
    ratio_test_java_files_command(sys.argv[1:])
