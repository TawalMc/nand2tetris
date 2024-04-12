from parser.constants import C_ARITHMETIC, C_RETURN
from parser.parser import Parser

if __name__ == '__main__':
    parser = Parser("../StackArithmetic/SimpleAdd/SimpleAdd.vm")
    while parser.has_more_lines():
        parser.advance()
        command = parser.command_type()
        if not command:
            continue
        if command != C_RETURN:
            print("ar:", parser.arg1())

    pass
