import xml.etree.ElementTree as ElT
from typing import List


class CompilationEngine:
    def __init__(self, in_file: str, out_file: str):
        self.__in_file = in_file
        self.__out_file = open(out_file, 'w+')

        self.__token_iterator = ElT.iterparse(self.__in_file)
        _, self.__current_token = next(self.__token_iterator)

        self.compile_class()

    def compile_class(self):
        self.__out_file.write("<class>\n")
        self.process(["class"])
        # more
        self.__out_file.write("</class>")

    def process(self, tokens: List[str]):
        if self.__current_token.text in tokens:
            self.write_token(self.__current_token.tag, self.__current_token.text)
        else:
            raise SyntaxError(f"found token: {self.__current_token.text} instead of {''.join(tokens)} ")

        _, self.__current_token = next(self.__token_iterator)

    def write_token(self, token_type: str, token):
        self.__out_file.write(f"<{token_type}>{token}</{token_type}>\n")

    def close(self):
        self.__out_file.close()
