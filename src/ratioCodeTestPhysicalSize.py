import os


def calculate_test_to_code_size_ratio():
    main_folder = 'jfreechart/src/main/java/org/jfree'
    test_folder = 'jfreechart/src/test/java/org/jfree'
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
    calculate_test_to_code_size_ratio()