import requests
from urllib.parse import parse_qs, urlparse
from git import Repo
import os
from pathlib import Path

# get latest version of jfreechart and place in same directory as the program
folder_path = 'jfreechart'
if not os.path.isdir(folder_path):
    Repo.clone_from('https://github.com/jfree/jfreechart.git', folder_path)


def get_comment_density():
    pass


def get_percent_methods_not_tested():
    pass


def calculate_csec():
    pass


def mentions(path_folder: Path, file_path: Path, class_name: str):
    full_path = Path.joinpath(path_folder, file_path)

    with open(full_path) as file:
        for line in file:
            if line[0] != '/' or line[1] != '/':
                if class_name in line:
                    return True

    return False


def calculate_test_to_code_size_ratio():
    main_folder = folder_path + '/src/main/java/org/jfree'
    test_folder = folder_path + '/src/test/java/org/jfree'
    size_test = 0
    size_code = 0

    for path, dir, files in os.walk(main_folder):
        for f in files:
            file_path = os.path.join(path, f)
            size_code += os.path.getsize(file_path)

    for path, dir, files in os.walk(test_folder):
        for f in files:
            file_path = os.path.join(path, f)
            size_test += os.path.getsize(file_path)

    return size_code / size_test


def get_number_of_commits():
    # Code from https://brianli.com/2022/07/python-get-number-of-commits-github-repository/#:~:text=As%20you%20can%20imagine%2C%20this,commits%20on%20each%20API%20call.
    owner = 'jfree'
    repo = 'jfreechart'

    url = 'https://api.github.com/repos/{}/{}/commits?per_page=1'.format(owner, repo)
    r = requests.get(url)
    links = r.links
    rel_last_link_url = urlparse(links["last"]["url"])
    rel_last_link_url_args = parse_qs(rel_last_link_url.query)
    rel_last_link_url_page_arg = rel_last_link_url_args["page"][0]
    commits_count = int(rel_last_link_url_page_arg)
    return commits_count


def main():
    print(calculate_test_to_code_size_ratio())
    print(get_number_of_commits())


if __name__ == "__main__":
    main()