from src.parser import writer
from src.parser.dictionary import Dictionary, DictionaryPage
from src.parser import reader

pages = reader.read_files()


dictionary_pages = [DictionaryPage(name=name, lines=lines) for name, lines in pages]

dictionary = Dictionary(dictionary_pages=dictionary_pages[0:50])

writer.write_dictionary_to_json_file(dictionary)
