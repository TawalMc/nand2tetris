import os
import sys

from code_writer.code_writer import CodeWriter
from constants import C_ARITHMETIC, C_PUSH, C_POP, C_LABEL, C_GOTO, C_IF, C_FUNCTION, C_RETURN
from parser.parser import Parser

if __name__ == '__main__':
    in_file = sys.argv[1]
    file_name = os.path.basename(in_file)

    if file_name[0].upper() != file_name[0]:
        raise ValueError("the file name must start with an uppercase letter")
    if file_name[-2:] != "vm":
        raise ValueError("the file extension must be 'vm'")
    out_file = in_file[: -2] + "asm"

    parser = Parser(in_file)
    writer = CodeWriter(out_file)
    while parser.has_more_lines():
        parser.advance()
        command_type = parser.command_type()
        if not command_type:
            continue

        if command_type == C_ARITHMETIC:
            writer.write_arithmetic(parser.arg1())
        elif command_type in [C_PUSH, C_POP]:
            writer.write_push_pop(parser.command(), parser.arg1(), int(parser.arg2()))
        elif command_type in [C_LABEL, C_GOTO, C_IF]:
            writer.write_label_if_goto(parser.command(), parser.arg1())
        elif command_type == C_FUNCTION:
            writer.write_function(parser.command(), parser.arg1(), int(parser.arg2()))
        elif command_type == C_RETURN:
            writer.write_return(parser.command(), parser.arg1())
        #     # print(f"{parser.current_command}: {parser.command()} - {parser.arg1()}")
        # print(f"{parser.current_command}: {parser.command()} - {parser.arg1()} - {parser.arg2()}")

    parser.close()
    writer.close()
