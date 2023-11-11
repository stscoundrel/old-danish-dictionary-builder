import os
from typing import Final

input_folder: Final[str] = "resources/text"
output_folder: Final[str] = "resources/parsed"


def read_files() -> list[list[str]]:
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pages: list[list[str]] = []

    files = [f for f in os.listdir(input_folder) if f.endswith(".txt")]

    for file in files:
        input_path = os.path.join(input_folder, file)

        with open(input_path, "r") as infile:
            lines = infile.readlines()
            pages.append(lines)

    return pages
