from constants import TEMP_ADDR


def arithmetic_operations(command, count):
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


class CodeWriter:
    def __init__(self, file_path: str):
        self.__count_ari_inst = 0
        self.__file = open(file_path, 'w+')

    def write_arithmetic(self, command):
        instructions = arithmetic_operations(command, self.__count_ari_inst)
        for inst in instructions:
            self.__file.write(f"{inst}\n")
        self.__count_ari_inst += 1

    def write_push_pop(self):
        pass

    def close(self):
        self.__file.close()
