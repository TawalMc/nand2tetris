import xml.etree.ElementTree as ElT
from typing import List

from utils.utils import write_avoid_xml_conflicts


class CompilationEngine:
    def __init__(self, in_file: str, out_file: str):
        self.__in_file = in_file
        self.__out_file = open(out_file, 'w+')

        self.__token_iterator = ElT.iterparse(self.__in_file)
        _, self.__current_token = next(self.__token_iterator)

    def compile_class(self):
        # 'class' className '{' classVarDec* subroutineDec* '}'
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
        while self.__current_token.text in ['constructor', 'function', 'method']:
            self.compile_subroutine_dec()

        # }
        self.process(["}"])

        self.__out_file.write("</class>")

    def compile_class_var_dec(self):
        # ( 'static' | 'field' ) type varName ( ',' varName)* ';'
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
        # ( 'constructor' | 'function' | 'method' ) ( 'void' | type) subroutineName '(' parameterList ')' subroutineBody
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
        self.compile_parameter_list()

        # )
        self.process([")"])

        # subroutineBody
        self.subroutine_body()

        self.__out_file.write("</subroutineDec>\n")

    def compile_parameter_list(self):
        # ((type varName) ( ',' type varName)*)?
        self.__out_file.write("<parameterList>\n")

        if self.__current_token.text != ")":
            # (type varName)
            self.process_terminal(["identifier"], ['int', 'char', 'boolean'])
            self.process_terminal(["identifier"])

            # (, type varName)*
            while self.__current_token.text == ",":
                self.process([","])

                self.process_terminal(["identifier"], ['int', 'char', 'boolean'])
                self.process_terminal(["identifier"])

        self.__out_file.write("</parameterList>\n")

    def subroutine_body(self):
        # '{' varDec* statements '}'
        self.__out_file.write("<subroutineBody>\n")

        # {
        self.process(["{"])

        # varDec*
        while self.__current_token.text == "var":
            self.compile_var_dec()

        # statements
        self.compile_statements()

        # }
        self.process(["}"])

        self.__out_file.write("</subroutineBody>\n")
        pass

    def compile_subroutine_call(self):
        # subroutineName '(' expressionList ')' | (className | varName) '.' subroutineName '(' expressionList ')'

        # subroutineName | className | varName
        # self.process_terminal(["identifier"])

        #  (className | varName) '.' subroutineName '(' expressionList ')'
        if self.__current_token.text == ".":
            # .
            self.process(["."])
            # subroutineName
            self.process_terminal(["identifier"])

        # (
        self.process(["("])

        # expressionList
        self.compile_expression_list()

        # )
        self.process([")"])

    def compile_var_dec(self):
        # 'var' type varName ( ',' varName)* ';'
        self.__out_file.write("<varDec>\n")

        # var
        self.process(["var"])

        # type
        self.process_terminal(["identifier"], ['int', 'char', 'boolean'])

        # varName
        self.process_terminal(["identifier"])

        # (, type varName)*
        while self.__current_token.text != ";":
            self.process([","])
            self.process_terminal(["identifier"])

        self.process([";"])

        self.__out_file.write("</varDec>\n")
        pass

    def compile_statements(self):
        # statement *
        self.__out_file.write("<statements>\n")

        while self.__current_token.text in ["if", "let", "while", "do", "return"]:
            if self.__current_token.text == "if":
                self.compile_if()
            elif self.__current_token.text == "let":
                self.compile_let()
            elif self.__current_token.text == "while":
                self.compile_while()
            elif self.__current_token.text == "do":
                self.compile_do()
            elif self.__current_token.text == "return":
                self.compile_return()

        self.__out_file.write("</statements>\n")

    def compile_expression_list(self):
        # (expression(',' expression) * )?
        self.__out_file.write("<expressionList>\n")

        while self.__current_token.text != ")":
            if self.__current_token.text == ",":
                self.process([","])
            self.compile_expression()

        self.__out_file.write("</expressionList>\n")

    # TODO: real implementation
    def compile_expression(self):
        # term (op term)*
        self.__out_file.write("<expression>\n")

        # term
        self.compile_term()

        # (op term)*
        while self.__current_token.text in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            self.process_terminal([], ['+', '-', '*', '/', '&', '|', '<', '>', '='])
            self.compile_term()

        self.__out_file.write("</expression>\n")
        pass

    # TODO: real implementation
    def compile_term(self):
        # integerConstant | stringConstant | keywordConstant |
        # varName | varName '[' expression ']' | subroutineCall |
        # '(' expression ')' | unaryOp term
        self.__out_file.write("<term>\n")

        # integerConstant | stringConstant | keywordConstant
        if self.__current_token.tag in ["integerConstant", "stringConstant"]:
            self.process_terminal(["integerConstant", "stringConstant"])

        elif self.__current_token.tag == "keyword":
            self.process(['true', 'false', 'null', 'this'])

        # '(' expression ')'
        elif self.__current_token.text == "(":
            self.process(["("])
            self.compile_expression()
            self.process([")"])

        # unaryOp term
        elif self.__current_token.text in ['-', '~']:
            self.process_terminal([], ['-', '~'])
            self.compile_term()

        elif self.__current_token.tag == "identifier":
            self.process_terminal(["identifier"])
            # varName '[' expression ']'
            if self.__current_token.text == "[":
                self.process(["["])
                self.compile_expression()
                self.process(["]"])
            # subroutineCall
            elif self.__current_token.text in [".", "("]:
                self.compile_subroutine_call()

        self.__out_file.write("</term>\n")

    def compile_let(self):
        # 'let' varName ( '[' expression ']' )? '=' expression ';'
        self.__out_file.write("<letStatement>\n")

        # let
        self.process(["let"])

        # varName
        self.process_terminal(["identifier"])

        # ( '[' expression ']' )?
        # case: [expression]
        if self.__current_token.text == "[":
            self.process(["["])
            self.compile_expression()
            self.process(["]"])

        # =
        self.process(["="])

        # expression
        self.compile_expression()

        # ;
        self.process([";"])

        self.__out_file.write("</letStatement>\n")

    def compile_if(self):
        # 'if' '(' expression ')' '{' statements '}'
        # ( 'else' '{' statements '}' )?
        self.__out_file.write("<ifStatement>\n")

        # if
        self.process(["if"])

        # (
        self.process(["("])

        # expression
        self.compile_expression()

        # )
        self.process([")"])

        # {
        self.process(["{"])

        # statements
        self.compile_statements()

        # }
        self.process(["}"])

        # else
        if self.__current_token.text == "else":
            self.process(["else"])
            # {
            self.process(["{"])
            # statements
            self.compile_statements()
            # }
            self.process(["}"])

        self.__out_file.write("</ifStatement>\n")

    def compile_while(self):
        # 'while' '(' expression ')' '{' statements '}'
        self.__out_file.write("<whileStatement>\n")

        # while
        self.process(["while"])

        # (
        self.process(["("])

        # expression
        self.compile_expression()

        # )
        self.process([")"])

        # {
        self.process(["{"])

        # statements
        self.compile_statements()

        # }
        self.process(["}"])

        self.__out_file.write("</whileStatement>\n")

    def compile_do(self):
        # 'do' subroutineCall ';'
        self.__out_file.write("<doStatement>\n")

        # do
        self.process(["do"])

        # subroutineCall
        # subroutineName | className | varName
        self.process_terminal(["identifier"])
        self.compile_subroutine_call()

        # ;
        self.process([";"])

        self.__out_file.write("</doStatement>\n")

    def compile_return(self):
        # 'return' expression? ';'
        self.__out_file.write("<returnStatement>\n")

        # return
        self.process(["return"])

        # expression
        if self.__current_token.text != ";":
            self.compile_expression()

        # ;
        self.process([";"])
        self.__out_file.write("</returnStatement>\n")

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
        self.__out_file.write(f"<{token_type}>{write_avoid_xml_conflicts(token)}</{token_type}>\n")

    def close(self):
        self.__out_file.close()
