import sys
from pathlib import Path

from JavaProjectClassEvaluation import JavaProjectClassEvaluation


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

    test_files = calculate_number_of_test_file(path_folder_test)
    evaluation = calculate_number_of_java_file(path_folder)

    print(f"Nombre de fichier test:{len(test_files)}")
    print(f"Nombre de public class:{len(evaluation.public_classes)}")
    print(f"Nombre de private class:{len(evaluation.private_classes)}")
    print(f"Nombre de interface:{len(evaluation.interface)}")
    print(f"Nombre de abstract class:{len(evaluation.abstract_classes)}")
    print(f"Nombre de autre( example enum) :{len(evaluation.other)}")

    number_of_class_not_test, number_of_interface_not_test, number_of_private_classes_not_test, number_of_abstract_classes_not_test = find_class_not_test(
        evaluation, test_files)
    print(f"Nombre de classes publique pas tester:{number_of_class_not_test}")
    print(f"Nombre de interfaces pas tester:{number_of_interface_not_test}")
    print(f"Nombre de classes privées pas tester:{number_of_private_classes_not_test}")
    print(f"Nombre de classes abstraites pas tester:{number_of_abstract_classes_not_test}")

    print(f"ratio publique = {number_of_class_not_test / len(evaluation.public_classes)}")
    print(f"ratio abstraites = {number_of_abstract_classes_not_test / len(evaluation.abstract_classes)}")
    print(
        f"ratio total = {(number_of_class_not_test + number_of_abstract_classes_not_test) / (len(evaluation.public_classes) + len(evaluation.abstract_classes))}")


def calculate_number_of_test_file(path: Path, test_files=[]):
    for file in path.iterdir():
        if file.is_dir():
            calculate_number_of_test_file(file, test_files)
        elif file.suffix.upper() == ".JAVA":
            class_name = file.stem
            if class_name[-4:] == "Test":
                class_name = class_name[:-4]

            test_files.append(class_name)

    return test_files


def calculate_number_of_java_file(path: Path, evaluation=JavaProjectClassEvaluation()):
    for file in path.iterdir():

        if file.is_dir():
            calculate_number_of_java_file(file, evaluation)

        elif file.suffix.upper() == ".JAVA":
            class_name = file.stem
            match find_file_type(file):
                case "class":
                    evaluation.public_classes.append(class_name)
                case "interface":
                    evaluation.interface.append(class_name)
                case "abstract":
                    evaluation.abstract_classes.append(class_name)
                case "private":
                    evaluation.private_classes.append(class_name)
                case _:
                    evaluation.other.append(class_name)

    return evaluation


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


def find_class_not_test(evaluation: JavaProjectClassEvaluation, list_tests):
    number_of_class_not_test = len(evaluation.public_classes) - len(
        set(evaluation.public_classes).intersection(list_tests))
    number_of_interface_not_test = len(evaluation.interface) - len(
        set(evaluation.interface).intersection(list_tests))
    number_of_private_classes_not_test = len(evaluation.private_classes) - len(
        set(evaluation.private_classes).intersection(list_tests))
    number_of_abstract_classes_not_test = len(evaluation.abstract_classes) - len(
        set(evaluation.abstract_classes).intersection(list_tests))

    return number_of_class_not_test, number_of_interface_not_test, number_of_private_classes_not_test, number_of_abstract_classes_not_test


if __name__ == "__main__":
    ratio_test_java_files_command(sys.argv[1:])
