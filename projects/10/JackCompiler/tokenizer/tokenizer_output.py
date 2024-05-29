from tokenizer.lexical_elements import TOKEN_XML


class TokenizerOutput:
    def __init__(self, out_file_path: str):
        self.__file = open(out_file_path, 'w+')

        self.__file.write("<tokens>\n")

    def write_token(self, token_type: str, token):
        tag = TOKEN_XML[token_type]
        self.__file.write(f"<{tag}>{token}</{tag}>\n")

    def close(self):
        self.__file.write("</tokens>\n")
        self.__file.close()
