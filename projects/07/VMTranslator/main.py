from parser.constants import C_ARITHMETIC, C_RETURN, C_PUSH, C_POP, C_FUNCTION, C_CALL
from parser.parser import Parser

if __name__ == '__main__':
    parser = Parser("../StackArithmetic/SimpleAdd/SimpleAdd.vm")
    while parser.has_more_lines():
        parser.advance()
        command = parser.command_type()
        if not command:
            continue
        print(parser.current_command)
        if command != C_RETURN:
            print("ar1:", parser.arg1())
        if command in [C_PUSH, C_POP, C_FUNCTION, C_CALL]:
            print("ar2:", parser.arg2())

    pass
