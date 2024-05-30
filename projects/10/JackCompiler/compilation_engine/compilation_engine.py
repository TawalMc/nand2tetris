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

        # class
        self.process(["class"])
        # className
        self.process_terminal(["identifier"])
        # {
        self.process(["{"])
        # classVarDec*
        while self.__current_token.text in ["static", "field"]:
            self.compile_class_var_dec()

        # subroutineDec*
        self.compile_subroutine_dec()

        # self.process(["}"])

        self.__out_file.write("</class>")

    def compile_class_var_dec(self):
        self.__out_file.write("<classVarDec>\n")

        # static | field
        self.process(["static", "field"])
        # type (int, char, boolean, className)
        self.process_terminal(["identifier"], ['int', 'char', 'boolean'])
        # varName
        self.process_terminal(["identifier"])
        # ( ',' varName)*
        while self.__current_token.text != ";":
            self.process([","])
            self.process_terminal(["identifier"])
        # ';'
        self.process([";"])

        self.__out_file.write("</classVarDec>\n")

    def compile_subroutine_dec(self):
        self.__out_file.write("<subroutineDec>\n")

        # ( 'constructor' | 'function' | 'method')
        self.process(['constructor', 'function', 'method'])

        # ( 'void' | type)
        self.process_terminal(["identifier"], ['int', 'char', 'boolean', 'void'])

        # subroutineName
        self.process_terminal(["identifier"])

        # (
        self.process(["("])

        # parameterList
        if self.__current_token.text != ")":
            self.compile_parameter_list()

        # )
        self.process([")"])

        self.__out_file.write("</subroutineDec>\n")

    def compile_parameter_list(self):
        self.__out_file.write("<parameterList>\n")

        # (type varName)
        self.process_terminal(["identifier"], ['int', 'char', 'boolean'])
        self.process_terminal(["identifier"])

        # (, type varName)*
        while self.__current_token.text == ",":
            self.process([","])

            self.process_terminal(["identifier"], ['int', 'char', 'boolean'])
            self.process_terminal(["identifier"])

        self.__out_file.write("</parameterList>\n")

    def process(self, tokens: List[str]):
        if self.__current_token.text in tokens:
            self.write_token(self.__current_token.tag, self.__current_token.text)
        else:
            raise SyntaxError(f"found token: {self.__current_token.text} instead of {''.join(tokens)} ")

        _, self.__current_token = next(self.__token_iterator)

    def process_terminal(self, token_types: List[str], token_values: List[str] = []):
        if self.__current_token.tag in token_types or self.__current_token.text in token_values:
            self.write_token(self.__current_token.tag, self.__current_token.text)
        else:
            raise SyntaxError(
                f"found token type: {self.__current_token.tag} and {self.__current_token.text} "
                f"instead of {''.join(token_types)} or {''.join(token_values)}")

        _, self.__current_token = next(self.__token_iterator)

    def write_token(self, token_type: str, token):
        self.__out_file.write(f"<{token_type}>{token}</{token_type}>\n")

    def close(self):
        self.__out_file.close()
