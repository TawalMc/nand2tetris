import xml.etree.ElementTree as ElT
from typing import List

from symbol_table.symbol_table import SymbolTable
from tokenizer.lexical_elements import IdentifierStatus, Kind, ARITHMETICS_OPS
from utils.utils import write_avoid_xml_conflicts
from vm_writer.vm_writer import VMWriter

file = "/home/tawaliou/Documents/apps/nand2tetris/projects/10/JackCompiler/test.txt"


class CompilationEngine:
    def __init__(self, in_file: str, out_file: str):
        self.__in_file = in_file
        self.__out_file = open(out_file, 'w+')

        self.__token_iterator = ElT.iterparse(self.__in_file)
        _, self.__current_token = next(self.__token_iterator)

        self.class_symbol_table = SymbolTable()
        self.subroutine_symbol_table = SymbolTable()
        self.vm_writer = VMWriter(file)

    def compile_class(self):
        # 'class' className '{' classVarDec* subroutineDec* '}'
        # self.__out_file.write("<class>\n")

        # class
        self.process(["class"])

        # className
        self.class_symbol_table.update_symbol_table_name(self.__current_token.text)
        self.process_terminal(token_types=["identifier"],
                              attribs={"kind": Kind.CLASS, "status": IdentifierStatus.DEFINED})
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

        # self.__out_file.write("</class>")

    def compile_class_var_dec(self):
        # ( 'static' | 'field' ) type varName ( ',' varName)* ';'
        # self.__out_file.write("<classVarDec>\n")

        # TODO: review implementation of "static"
        # static | field
        _token_kind = self.__current_token.text
        self.process(["static", "field"])

        # type (int, char, boolean, className)
        _token_type = self.__current_token.text
        self.process_terminal(["identifier"], ['int', 'char', 'boolean'],
                              {"kind": Kind.CLASS, 'status': IdentifierStatus.USED})
        # varName
        _var_name = self.class_symbol_table.define(self.__current_token.text, _token_type, _token_kind)
        self.process_terminal(
            token_types=["identifier"],
            attribs={"kind": _token_kind,
                     "status": IdentifierStatus.DEFINED,
                     "type": _token_type,
                     "index": _var_name['index']})

        # ( ',' varName)*
        while self.__current_token.text != ";":
            self.process([","])

            _var_name = self.class_symbol_table.define(self.__current_token.text, _token_type, _token_kind)
            self.process_terminal(
                token_types=["identifier"],
                attribs={"kind": _token_kind,
                         "status": IdentifierStatus.DEFINED,
                         "type": _token_type,
                         "index": _var_name['index']}
            )
        # ';'
        self.process([";"])

        # self.__out_file.write("</classVarDec>\n")

    def compile_subroutine_dec(self):
        # call SymbolTable subroutine symbol table init
        self.subroutine_symbol_table.reset()

        # ( 'constructor' | 'function' | 'method' ) ( 'void' | type) subroutineName '(' parameterList ')' subroutineBody
        # self.__out_file.write("<subroutineDec>\n")

        # ( 'constructor' | 'function' | 'method')
        _is_constructor = self.__current_token.text == "constructor"
        self.process(['constructor', 'function', 'method'])

        # ( 'void' | type)
        _token_type = self.__current_token.text
        self.process_terminal(
            ["identifier"],
            ['int', 'char', 'boolean', 'void'],
            {"kind": Kind.CLASS, "status": IdentifierStatus.USED}
        )

        # subroutineName

        self.subroutine_symbol_table.update_symbol_table_name(self.__current_token.text)
        self.process_terminal(
            token_types=["identifier"],
            attribs={"kind": Kind.ROUTINE, "type": _token_type, "status": IdentifierStatus.DEFINED})

        # (
        self.process(["("])

        # parameterList
        if not _is_constructor:
            self.subroutine_symbol_table.define(Kind.THIS, self.class_symbol_table.table_name(), Kind.ARG)
        self.compile_parameter_list()

        # )
        self.process([")"])

        # VMCode for function
        self.vm_writer.write_function(
            f"{self.class_symbol_table.table_name()}.{self.subroutine_symbol_table.table_name()}",
            self.subroutine_symbol_table.var_count(Kind.ARG)
        )
        # VMCode for constructor
        if _is_constructor:
            self.vm_writer.write_push(Kind.CONST, self.class_symbol_table.var_count(Kind.FIELD))
            self.vm_writer.write_call("Memory.alloc", 1)
            self.vm_writer.write_pop(Kind.POINTER, 0)
        else:
            self.vm_writer.write_push(Kind.ARG, 0)
            self.vm_writer.write_pop(Kind.POINTER, 0)

        # subroutineBody
        self.subroutine_body()

        # self.__out_file.write("</subroutineDec>\n")
        if _token_type == "void":
            self.vm_writer.write_push(Kind.CONST, 0)
        self.vm_writer.write_return()

    def compile_parameter_list(self):
        # call symbol table subroutine

        # ((type varName) ( ',' type varName)*)?
        # self.__out_file.write("<parameterList>\n")

        if self.__current_token.text != ")":
            # (type varName)
            _token_type = self.__current_token.text
            self.process_terminal(
                ["identifier"],
                ['int', 'char', 'boolean'],
                {"kind": Kind.CLASS, "status": IdentifierStatus.USED}
            )

            _var_name = self.subroutine_symbol_table.define(self.__current_token.text, _token_type, Kind.ARG)
            self.process_terminal(
                token_types=["identifier"],
                attribs={"kind": Kind.ARG,
                         "status": IdentifierStatus.DEFINED,
                         "type": _token_type,
                         "index": _var_name['index']}
            )

            # (, type varName)*
            while self.__current_token.text == ",":
                self.process([","])

                _token_type = self.__current_token.text
                self.process_terminal(
                    ["identifier"],
                    ['int', 'char', 'boolean'],
                    {"kind": Kind.CLASS, "status": IdentifierStatus.USED}
                )

                _var_name = self.subroutine_symbol_table.define(self.__current_token.text, _token_type, Kind.ARG)
                self.process_terminal(
                    token_types=["identifier"],
                    attribs={"kind": Kind.ARG,
                             "status": IdentifierStatus.DEFINED,
                             "type": _token_type,
                             "index": _var_name['index']}
                )

        # self.__out_file.write("</parameterList>\n")

    def subroutine_body(self):
        # '{' varDec* statements '}'
        # self.__out_file.write("<subroutineBody>\n")

        # {
        self.process(["{"])

        # call symbol table subroutine
        # varDec*
        while self.__current_token.text == "var":
            self.compile_var_dec()

        # statements
        self.compile_statements()

        # }
        self.process(["}"])

        # self.__out_file.write("</subroutineBody>\n")
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
            self.process_terminal(
                token_types=["identifier"],
                attribs={"kind": Kind.ROUTINE, "status": IdentifierStatus.USED}
            )

        # (
        self.process(["("])

        # expressionList
        self.compile_expression_list()

        # )
        self.process([")"])

    def compile_var_dec(self):
        # 'var' type varName ( ',' varName)* ';'
        # self.__out_file.write("<varDec>\n")

        # var
        self.process(["var"])

        # type
        _token_type = self.__current_token.text
        self.process_terminal(
            ["identifier"],
            ['int', 'char', 'boolean'],
            {"kind": Kind.CLASS, "status": IdentifierStatus.USED}
        )

        # varName
        _var_name = self.class_symbol_table.define(self.__current_token.text, _token_type, Kind.LOCAL)
        self.process_terminal(
            token_types=["identifier"],
            attribs={"kind": Kind.LOCAL,
                     "status": IdentifierStatus.DEFINED,
                     "type": _token_type,
                     "index": _var_name['index']}
        )

        # (, type varName)*
        while self.__current_token.text != ";":
            self.process([","])

            _var_name = self.class_symbol_table.define(self.__current_token.text, _token_type, Kind.LOCAL)
            self.process_terminal(
                token_types=["identifier"],
                attribs={"kind": Kind.LOCAL,
                         "status": IdentifierStatus.DEFINED,
                         "type": _token_type,
                         "index": _var_name['index']}
            )

        self.process([";"])

        # self.__out_file.write("</varDec>\n")
        pass

    def compile_statements(self):
        # statement *
        # self.__out_file.write("<statements>\n")

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

        # self.__out_file.write("</statements>\n")

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
        # self.__out_file.write("<expression>\n")

        # term
        self.compile_term()

        # (op term)*
        while self.__current_token.text in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            _arithmetic_op = self.__current_token.text
            self.process_terminal([], ['+', '-', '*', '/', '&', '|', '<', '>', '='])
            self.compile_term()

            # vm code
            self.vm_writer.write_arithmetic(ARITHMETICS_OPS[_arithmetic_op])

        # self.__out_file.write("</expression>\n")
        pass

    # TODO: real implementation
    def compile_term(self):
        # integerConstant | stringConstant | keywordConstant |
        # varName | varName '[' expression ']' | subroutineCall |
        # '(' expression ')' | unaryOp term
        # self.__out_file.write("<term>\n")

        # integerConstant | stringConstant | keywordConstant
        if self.__current_token.tag in ["integerConstant", "stringConstant"]:
            _token_text = self.__current_token.text
            self.process_terminal(["integerConstant", "stringConstant"])
            if _token_text == "integerConstant":
                self.vm_writer.write_push(Kind.CONST, _token_text)
            # else:


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

        # routine symbol table call
        elif self.__current_token.tag == "identifier":
            _attribs = {"status": IdentifierStatus.USED, "kind": Kind.CLASS}
            _symbol_table = None
            if self.subroutine_symbol_table.is_key(self.__current_token.text):
                _symbol_table = self.subroutine_symbol_table
            elif self.class_symbol_table.is_key(self.__current_token.text):
                _symbol_table = self.class_symbol_table

            if _symbol_table:
                _attribs = {**_attribs, "kind": _symbol_table.kind_of(self.__current_token.text),
                            'type': _symbol_table.type_of(self.__current_token.text),
                            'index': _symbol_table.index_of(self.__current_token.text)}

            self.process_terminal(token_types=["identifier"], attribs=_attribs)

            # varName '[' expression ']'
            if self.__current_token.text == "[":
                self.process(["["])
                self.compile_expression()
                self.process(["]"])
            # subroutineCall
            elif self.__current_token.text in [".", "("]:
                self.compile_subroutine_call()

        # self.__out_file.write("</term>\n")

    def compile_let(self):
        # 'let' varName ( '[' expression ']' )? '=' expression ';'
        self.__out_file.write("<letStatement>\n")

        # let
        self.process(["let"])

        # varName
        if self.subroutine_symbol_table.is_key(self.__current_token.text):
            _symbol_table = self.subroutine_symbol_table
        else:
            _symbol_table = self.class_symbol_table

        self.process_terminal(
            token_types=["identifier"],
            attribs={"status": IdentifierStatus.USED,
                     "kind": _symbol_table.kind_of(self.__current_token.text),
                     'type': _symbol_table.type_of(self.__current_token.text),
                     'index': _symbol_table.index_of(self.__current_token.text)})

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
        # self.__out_file.write("<ifStatement>\n")

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

        # self.__out_file.write("</ifStatement>\n")

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
        _symbol_table = None
        _attribs = {"kind": f"{Kind.CLASS}|{Kind.ROUTINE}", "status": IdentifierStatus.USED}
        if self.subroutine_symbol_table.is_key(self.__current_token.text):
            _symbol_table = self.subroutine_symbol_table
        elif self.class_symbol_table.is_key(self.__current_token.text):
            _symbol_table = self.class_symbol_table

        if _symbol_table:
            _attribs = {"kind": _symbol_table.kind_of(self.__current_token.text),
                        "status": IdentifierStatus.USED,
                        'type': _symbol_table.type_of(self.__current_token.text),
                        'index': _symbol_table.index_of(self.__current_token.text)}

        self.process_terminal(
            token_types=["identifier"],
            attribs=_attribs
        )
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
            _, self.__current_token = next(self.__token_iterator)
            # self.write_token(self.__current_token.tag, self.__current_token.text)
        else:
            raise SyntaxError(f"found token: {self.__current_token.text} instead of {''.join(tokens)} ")

    # if identifier:
    # <identifier kind="KIND" index="0" status="DEFINED|USED">_the_identifier_</identifier>
    def process_terminal(self, token_types: List[str], token_values: List[str] = [], attribs=None):
        if self.__current_token.tag in token_types or self.__current_token.text in token_values:
            _, self.__current_token = next(self.__token_iterator)
            # self.write_token(
            #     self.__current_token.tag,
            #     self.__current_token.text,
            #     '' if self.__current_token.tag != "identifier" else format_dict_to_str(attribs))
        else:
            raise SyntaxError(
                f"found token type: {self.__current_token.tag} and {self.__current_token.text} "
                f"instead of {''.join(token_types)} or {''.join(token_values)}")

    def write_token(self, token_type: str, token: str, attribs: str = ''):
        self.__out_file.write(f"<{token_type} {attribs}>{write_avoid_xml_conflicts(token)}</{token_type}>\n")
        pass

    def close(self):
        self.__out_file.close()
