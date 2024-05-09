import os
import sys

from code_writer.code_writer import CodeWriter
from constants import C_ARITHMETIC, C_PUSH, C_POP, C_LABEL, C_GOTO, C_IF, C_FUNCTION, C_RETURN
from parser.parser import Parser
from source_handler.source_handler import SourceHandler

if __name__ == '__main__':
    in_file = sys.argv[1]
    source_handler = SourceHandler(in_file)
    writer = CodeWriter(source_handler.out_file())

    for vm_file in source_handler.source_files():
        file_name = os.path.basename(vm_file)
        writer.write_new_vm_file(file_name)
        parser = Parser(vm_file)
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
                writer.write_branching(parser.command(), parser.arg1())
            elif command_type == C_FUNCTION:
                writer.write_function(parser.command(), parser.arg1(), int(parser.arg2()))
            elif command_type == C_RETURN:
                writer.write_return(parser.command(), parser.arg1())

        parser.close()

    writer.close()
