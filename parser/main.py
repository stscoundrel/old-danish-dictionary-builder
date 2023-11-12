from parser.src.parser import columns
from parser.src.parser import reader

pages = reader.read_files()
parsed = columns.parse_columns(pages)

print(pages[0])
print("-----------------------------")
print(parsed[0])
