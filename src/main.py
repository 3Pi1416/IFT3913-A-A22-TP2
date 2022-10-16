import os
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import requests
from git import Repo

# get latest version of jfreechart and place in same directory as the program
folder_path = 'jfreechart'
if not os.path.isdir(folder_path):
    Repo.clone_from('https://github.com/jfree/jfreechart.git', folder_path)


def get_comment_density(): #Maggie
    pass


def get_percent_methods_not_tested(): #Hugo
    pass


def calculate_csec(): #Maggie
    pass


def calculate_test_to_code_size_ratio(): #Maggie
    pass


# TODO: change pour chaque module
def get_number_of_commits(): #Hugo
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


def get_lines_of_code_added_per_commit_stats(): #Hugo
    pass


def main():
    print(calculate_test_to_code_size_ratio())
    print(get_number_of_commits())


if __name__ == "__main__":
    main()