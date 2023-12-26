import json

from src.parser.dictionary import Dictionary


def write_dictionary_to_json_file(dictionary: Dictionary) -> None:
    entries = dictionary.get_entries()

    json_entries = json.dumps([entry.to_json() for entry in entries], indent=2)

    file_path = "dictionary.json"

    # Open the file in write mode and write the JSON string to it
    with open(file_path, "w") as json_file:
        json_file.write(json_entries)
