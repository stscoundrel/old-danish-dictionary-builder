def open_test_file(file: str) -> list[str]:
    with open(f"./tests/test_data/{file}", "r") as infile:
        return infile.readlines()
