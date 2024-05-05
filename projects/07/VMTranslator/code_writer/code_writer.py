import os
from typing import Optional

from constants import TEMP_ADDR


def arithmetic_operations(command: str, count: int):
    operations = {
        "add": ["@SP", "A=M-1", "D=M", "A=A-1", "M=M+D", "@SP", "M=M-1"],
        "sub": ["@SP", "A=M-1", "D=M", "A=A-1", "M=M-D", "@SP", "M=M-1"],
        "neg": ["@SP", "A=M-1", "M=-M"],
        "eq": ["@SP", "A=M-1", "D=M", "A=A-1", "D=M-D", f"@EQ_{count}", "D;JEQ", "@SP", "A=M-1", "A=A-1", "M=0",
               f"@END_EQ_{count}", "0;JMP", f"(EQ_{count})", "@SP", "A=M-1", "A=A-1", "M=-1", f"(END_EQ_{count})",
               "@SP", "M=M-1"],
        "gt": ["@SP", "A=M-1", "D=M", "A=A-1", "D=M-D", f"@GT_{count}", "D;JGT", "@SP", "A=M-1", "A=A-1", "M=0",
               f"@END_GT_{count}", "0;JMP", f"(GT_{count})", "@SP", "A=M-1", "A=A-1", "M=-1", f"(END_GT_{count})",
               "@SP", "M=M-1"],
        "lt": ["@SP", "A=M-1", "D=M", "A=A-1", "D=M-D", f"@LT_{count}", "D;JLT", "@SP", "A=M-1", "A=A-1", "M=0",
               f"@END_LT_{count}", "0;JMP", f"(LT_{count})", "@SP", "A=M-1", "A=A-1", "M=-1", f"(END_LT_{count})",
               "@SP", "M=M-1"],
        "and": ["@SP", "A=M-1", "D=M", "A=A-1", "M=M&D", "@SP", "M=M-1"],
        "or": ["@SP", "A=M-1", "D=M", "A=A-1", "M=M|D", "@SP", "M=M-1"],
        "not": ["@SP", "A=M-1", "M=!M"]
    }
    return operations.get(command, [])


def push_pop_operations(file_name: str, command: str, segment: str, index_or_value: int):
    operations = {
        "constant": {
            "push": [f"@{index_or_value}", "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
        },
        "local": {
            "push": [f"@{index_or_value}", "D=A", "@LCL", "A=M+D", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"],
            "pop": [f"@{index_or_value}", "D=A", "@LCL", "D=M+D", "@addr", "M=D", "@SP", "A=M-1", "D=M", "@addr", "A=M",
                    "M=D", "@SP",
                    "M=M-1"]
        },
        "argument": {
            "push": [f"@{index_or_value}", "D=A", "@ARG", "A=M+D", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"],
            "pop": [f"@{index_or_value}", "D=A", "@ARG", "D=M+D", "@addr", "M=D", "@SP", "A=M-1", "D=M", "@addr", "A=M",
                    "M=D", "@SP", "M=M-1"]
        },
        "this": {
            "push": [f"@{index_or_value}", "D=A", "@THIS", "A=M+D", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"],
            "pop": [f"@{index_or_value}", "D=A", "@THIS", "D=M+D", "@addr", "M=D", "@SP", "A=M-1", "D=M", "@addr",
                    "A=M", "M=D", "@SP", "M=M-1"]
        },
        "that": {
            "push": [f"@{index_or_value}", "D=A", "@THAT", "A=M+D", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"],
            "pop": [f"@{index_or_value}", "D=A", "@THAT", "D=M+D", "@addr", "M=D", "@SP", "A=M-1", "D=M", "@addr",
                    "A=M", "M=D", "@SP", "M=M-1"]
        },
        "static": {
            "push": [f"@{file_name}.{index_or_value}", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"],
            "pop": ["@SP", "A=M-1", "D=M", f"@{file_name}.{index_or_value}", "M=D", "@SP", "M=M-1"]
        },
        "temp": {
            "push": [f"@{TEMP_ADDR + index_or_value}", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"],
            "pop": ["@SP", "A=M-1", "D=M", f"@{TEMP_ADDR + index_or_value}", "M=D", "@SP", "M=M-1"]
        },
        "pointer": {
            "push": [f"@{'THIS' if index_or_value == 0 else 'THAT'}", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"],
            "pop": ["@SP", "A=M-1", "D=M", f"@{'THIS' if index_or_value == 0 else 'THAT'}", "M=D", "@SP", "M=M-1"]
        }
    }
    return operations.get(segment, {}).get(command, [])


def branching_operations(command: str,
                         symbol: str,
                         n_args_or_vars: Optional[int] = None,
                         curr_func: Optional[str] = None,
                         count: int = 0):
    label_prefix = curr_func + '$' if curr_func else 'null$'

    operations = {
        "label": [f"({label_prefix}{symbol})"],
        "goto": [f"@{label_prefix}{symbol}", "0;JMP"],
        "if-goto": ["@SP", "A=M-1", "D=M", "@SP", "M=M-1", f"@{label_prefix}{symbol}", "D;JNE"],
        "function": [f"({symbol})", f"@{symbol}$i", "M=0", f"({symbol}$LOOP_{count})", f"@{n_args_or_vars}", "D=A",
                     f"@{symbol}.i", "D=M-D", f"@{symbol}$END_LOOP_{count}", "D;JLE", "@SP", "A=M", "M=0", "@SP",
                     "M=M+1", f"@{symbol}$i", "M=M+1", f"@{symbol}$LOOP_{count}", "0; JMP",
                     f"({symbol}$END_LOOP_{count})"],
        "return": ["@LCL", "D=M", f"@{label_prefix}END_FRAME", "M=D", "@5", "D=A", f"@{label_prefix}END_FRAME", "A=M-D",
                   "D=M",
                   f"@{label_prefix}RET_ADDR", "M=D",
                   "@SP", "A=M", "D=M", "@ARG", "A=M", "M=D", "@1", "D=A", f"@{label_prefix}END_FRAME", "A=M-D", "D=M",
                   "@THAT", "M=D",
                   "@1", "D=A", f"@{label_prefix}END_FRAME", "A=M-D", "D=M", "@THIS", "M=D", "@3", "D=A",
                   f"@{label_prefix}END_FRAME", "A=M-D", "D=M",
                   "@ARG", "M=D", "@4", "D=A", f"@{label_prefix}END_FRAME", "A=M-D", "D=M", "@LCL", "M=D",
                   f"@{label_prefix}RET_ADDR",
                   "0;JMP"]

    }

    return operations.get(command, [])


class CodeWriter:
    def __init__(self, file_path: str):
        self.__count_ari_inst = 0
        self.__count_branch_inst = 0
        self.__file = open(file_path, 'w+')
        self.__file_name = os.path.splitext(os.path.basename(file_path))[0]
        self.__curr_func: Optional[str] = None

    def write_arithmetic(self, command: str):
        instructions = arithmetic_operations(command, self.__count_ari_inst)
        for inst in instructions:
            self.__file.write(f"{inst}\n")
        self.__count_ari_inst += 1

    def write_push_pop(self, command: str, segment: str, index_or_value: int):
        instructions = push_pop_operations(self.__file_name, command, segment, index_or_value)
        for inst in instructions:
            self.__file.write(f"{inst}\n")

    def write_label_if_goto(self, command: str, symbol: str):
        instructions = branching_operations(command, symbol, None, self.__curr_func)
        for inst in instructions:
            self.__file.write(f"{inst}\n")

    def write_function(self, command: str, symbol: str, n_vars: int):
        instructions = branching_operations(command, symbol, n_vars, symbol, self.__count_branch_inst)
        for inst in instructions:
            self.__file.write(f"{inst}\n")
        self.__curr_func = symbol
        self.__count_branch_inst += 1

    def write_return(self, command: str, symbol: str):
        instructions = branching_operations(command, symbol, None, self.__curr_func)
        for inst in instructions:
            self.__file.write(f"{inst}\n")

        self.__curr_func = None

    def close(self):
        self.__file.close()
