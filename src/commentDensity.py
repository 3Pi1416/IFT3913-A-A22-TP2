import os
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import statistics


def comment_density_command(args):
    if len(args) != 1:
        print("Expected one directory as input.")
        return

    main_folder = Path(args[0])
    if not main_folder.is_dir():
        print(f"{main_folder} is not a folder.")
        return

    file_comment_density, list_line_comment, list_non_empty = read_comment_density_in_every_files(main_folder)
    generate_density_graph(list_line_comment, list_non_empty)
    comment_density_stats(file_comment_density)


def read_comment_density_in_every_files(path: Path, file_comment_density=[], list_line_comment=[], list_non_empty=[]):
    for file in path.iterdir():
        if file.is_dir():
            read_comment_density_in_every_files(file, file_comment_density, list_line_comment, list_non_empty)
        elif file.suffix.upper() == ".JAVA":
            num_lines_of_comments, num_non_empty_lines, density_of_comments = calculate_file_comment_density(file)
            file_comment_density.append(density_of_comments)
            list_line_comment.append(num_lines_of_comments)
            list_non_empty.append(num_non_empty_lines)

    return file_comment_density, list_line_comment, list_non_empty


def calculate_file_comment_density(file: Path):
    if not file.is_file() or file.suffix != '.java':
        raise Exception("Not a java file!")

    num_non_empty_lines = 0
    num_lines_of_comments = 0
    with open(file) as open_file:
        for line in open_file:
            if line.strip().replace("\n", ""):
                num_non_empty_lines += 1

            stripped_line = line.strip()
            if stripped_line:
                if stripped_line[:2] == '/*' or stripped_line[:2] == '//' or stripped_line[0] == '*':
                    num_lines_of_comments += 1

    return num_lines_of_comments, num_non_empty_lines, (num_lines_of_comments / num_non_empty_lines)


def generate_density_graph(file_sizes: list, comment_densities: list):
    x_points = np.array(file_sizes)
    y_points = np.array(comment_densities)
    plt.xlabel("File size in bytes")
    plt.ylabel("Density of comments")
    plt.scatter(x_points, y_points)
    plt.savefig("comment_density.png")


def comment_density_stats(density_list: list):
    density_list = list(filter(lambda i: i is not None, density_list))
    print(f"Median density: {statistics.median(density_list)}")
    print(f"Average density: {statistics.mean(density_list)}")
    print(f"STD dev of densities: {statistics.stdev(density_list)}")
    print(f"Min density: {min(density_list)}")
    print(f"Max density: {max(density_list)}")


if __name__ == "__main__":
    comment_density_command(sys.argv[1:])
