# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys

from compilation_engine.compilation_engine import CompilationEngine
from source_handler.source_handler import SourceHandler
from tokenizer.tokenizer import Tokenizer

if __name__ == '__main__':
    in_file = sys.argv[1]

    print("--- Start Tokenization ---")
    tokenizer_source_handler = SourceHandler(in_file, ".jack", "OwnT.xml")
    for jack_file in tokenizer_source_handler.out_files():
        print(f"tokenization: {jack_file['in']} --to-> {jack_file['out']}")
        tokenizer = Tokenizer(jack_file["in"], jack_file["out"])
        tokenizer.generate_tokens()
        tokenizer.close()
    print("--- End Tokenization ---")

    print("--- Start Parsing ---")
    parser_source_handler = SourceHandler(in_file, "OwnT.xml", "OwnP.xml")
    for tokens_file in parser_source_handler.out_files():
        print(f"parsing : {tokens_file['in']} --to-> {tokens_file['out']}")
        parser = CompilationEngine(tokens_file["in"], tokens_file["out"])
        parser.compile_class()
        parser.close()
    print("--- End Parsing ---")
