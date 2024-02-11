import re
from typing import List
import os

def read_prog(file: str) -> List[str]:
    """
    Read an assembly code from "file" and remove comments+whitespaces
    """
    prog_table = []

    prog = open(file, 'r')
    for line in prog:
        if line and not line.startswith("//"):  # exclude code started with comments
            line_splitted = line.split("//")
            code = re.sub(r"\s+", "", line_splitted[0])
            if code:
                prog_table.append(code)
    prog.close()
    return prog_table

def represents_int(s):
    try: 
        int(s)
    except ValueError:
        return False
    else:
        return True