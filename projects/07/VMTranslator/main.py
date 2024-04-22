from code_writer.code_writer import CodeWriter
from constants import C_ARITHMETIC
from parser.parser import Parser

if __name__ == '__main__':
    parser = Parser("../StackArithmetic/StackTest/StackTest.vm")
    # parser = Parser("../StackArithmetic/SimpleAdd/SimpleAdd.vm")
    writer = CodeWriter("assets/test.asm")

    while parser.has_more_lines():
        parser.advance()
        command_type = parser.command_type()
        if not command_type:
            continue
        # print(parser.current_command)
        # if command != C_RETURN:
        #     print("ar1:", parser.arg1())
        # if command in [C_PUSH, C_POP, C_FUNCTION, C_CALL]:
        #     print("ar2:", parser.arg2())
        if command_type == C_ARITHMETIC:
            writer.write_arithmetic(parser.arg1())

    parser.close()

    pass
