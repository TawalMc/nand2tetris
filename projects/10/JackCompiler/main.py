# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from compilation_engine.compilation_engine import CompilationEngine

if __name__ == '__main__':
    # in_file = sys.argv[1]
    # source_handler = SourceHandler(in_file, True)
    #
    # for jack_file in source_handler.out_files():
    #     tokenizer = Tokenizer(jack_file["in"])
    #     tokenizer_output = TokenizerOutput(jack_file["out"])
    #     while tokenizer.has_more_lines():
    #         tokenizer.read_line()
    #
    #         while tokenizer.has_more_tokens():
    #             tokenizer.advance()
    #             if tokenizer.get_current_token():
    #                 token_info = tokenizer.token_info()
    #                 tokenizer_output.write_token(token_info[0], token_info[1])
    #
    #     tokenizer.close()
    #     tokenizer_output.close()
    parser = CompilationEngine(
        "/home/tawaliou/Documents/apps/nand2tetris/projects/10/Square/SquareT.xml",
        "/home/tawaliou/Documents/apps/nand2tetris/projects/10/Square/SquareOwnP.xml"
    )

