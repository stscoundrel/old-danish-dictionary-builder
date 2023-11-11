from src.parser import reader, parser

pages = reader.read_files()
parsed = parser.parse_columns(pages)

print(pages[0])
print("-----------------------------")
print(parsed[0])
