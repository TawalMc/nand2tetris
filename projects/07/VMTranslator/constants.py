C_ARITHMETIC = "C_ARITHMETIC"
C_PUSH = "C_PUSH"
C_POP = "C_POP"
C_LABEL = "C_LABEL"
C_GOTO = "C_GOTO"
C_IF = "C_IF"
C_FUNCTION = "C_FUNCTION"
C_RETURN = "C_RETURN"
C_CALL = "C_CALL"

commands = {
    "add": C_ARITHMETIC,
    "sub": C_ARITHMETIC,
    "neg": C_ARITHMETIC,
    "eq": C_ARITHMETIC,
    "gt": C_ARITHMETIC,
    "lt": C_ARITHMETIC,
    "and": C_ARITHMETIC,
    "or": C_ARITHMETIC,
    "not": C_ARITHMETIC,
    "push": C_PUSH,
    "pop": C_POP,
    "label": C_LABEL,
    "goto": C_GOTO,
    "if-goto": C_IF,
    "Function": C_FUNCTION,
    "Call": C_CALL,
    "return": C_RETURN
}

COUNT_ARI_INST = 0


def arithmetic_instructions(command, count):
    if command == "add":
        return ["@SP", "A=M-1", "D=M", "A=A-1", "M=M+D", "@SP", "M=M-1"]
    if command == "sub":
        return ["@SP", "A=M-1", "D=M", "A=A-1", "M=M-D", "@SP", "M=M-1"]
    if command == "neg":
        return ["@SP", "A=M-1", "M=-M"]
    if command == "eq":
        return ["@SP", "A=M-1", "D=M", "A=A-1", "D=M-D", f"@EQ_{count}", "D;JEQ", "@SP", "A=M-1", "A=A-1", "M=0",
                f"@END_EQ_{count}", "0;JMP", f"(EQ_{count})", "@SP", "A=M-1", "A=A-1", "M=1", f"(END_EQ_{count})",
                "@SP", "M=M-1"]
    if command == "gt":
        return ["@SP", "A=M-1", "D=M", "A=A-1", "D=M-D", f"@GT_{count}", "D;JGT", "@SP", "A=M-1", "A=A-1", "M=0",
                f"@END_GT_{count}", "0;JMP", f"(GT_{count})", "@SP", "A=M-1", "A=A-1", "M=1", f"(END_GT_{count})",
                "@SP", "M=M-1"]
    if command == "lt":
        return ["@SP", "A=M-1", "D=M", "A=A-1", "D=M-D", f"@LT_{count}", "D;JLT", "@SP", "A=M-1", "A=A-1", "M=0",
                f"@END_LT_{count}", "0;JMP", f"(LT_{count})", "@SP", "A=M-1", "A=A-1", "M=1", f"(END_LT_{count})",
                "@SP", "M=M-1"]
