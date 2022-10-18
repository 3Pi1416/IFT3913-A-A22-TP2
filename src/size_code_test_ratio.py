import os


def calculate_test_to_code_size_ratio(folder_path):
    main_folder = folder_path + '/src/main/java/org/jfree'
    test_folder = folder_path + '/src/test/java/org/jfree'
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

    return size_code / size_test
