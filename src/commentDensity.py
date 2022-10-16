import os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import statistics


def comment_density():
    main_folder = 'jfreechart/src/main/java/org/jfree'
    file_comment_density = []
    file_size = []

    for path, dir, files in os.walk(main_folder):
        for f in files:
            file_path = os.path.join(path, f)
            file_size.append(os.path.getsize(file_path))
            file_comment_density.append(get_file_comment_density(Path(file_path)))

    generate_density_graph(file_size, file_comment_density)
    comment_density_stats(file_comment_density)


def get_file_comment_density(file: Path):
    if not file.is_file():
        raise Exception("Not a file!")
    if file.suffix != '.java':
        return

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

    return num_lines_of_comments / num_non_empty_lines


def generate_density_graph(file_sizes: list, comment_densities: list):
    x_points = np.array(file_sizes)
    y_points = np.array(comment_densities)
    plt.xlabel("File size in bytes")
    plt.ylabel("Density of comments")
    plt.scatter(x_points, y_points)
    plt.savefig("output/comment_density.png")


def comment_density_stats(density_list: list):
    density_list = list(filter(lambda i: i is not None, density_list))
    print(f"Median density: {statistics.median(density_list)}")
    print(f"Average density: {statistics.mean(density_list)}")
    print(f"STD dev of densities: {statistics.stdev(density_list)}")
    print(f"Min density: {min(density_list)}")
    print(f"Max density: {max(density_list)}")
