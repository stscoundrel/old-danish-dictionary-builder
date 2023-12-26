import os
from typing import Final

input_folder: Final[str] = "resources/text"
output_folder: Final[str] = "resources/parsed"


def read_files() -> list[tuple[str, list[str]]]:
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pages: list[tuple[str, list[str]]] = []

    unordered_files = [f for f in os.listdir(input_folder) if f.endswith(".txt")]
    files = sorted(unordered_files, key=lambda x: int(x.split("-")[0]))

    for file in files:
        filename = file.split("/")[-1]
        input_path = os.path.join(input_folder, file)

        with open(input_path, "r") as infile:
            lines = infile.readlines()
            pages.append((filename, lines))

    return pages
