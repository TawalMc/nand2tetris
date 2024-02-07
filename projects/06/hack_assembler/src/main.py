import re
from tables import LoadTables, SymbolTable
from utils import read_prog

progs = [
    "/home/tawaliou/Documents/apps/nand2tetris/projects/04/fill/Fill.asm",
]

tables = [
    "/home/tawaliou/Documents/apps/nand2tetris/projects/06/hack_assembler/src/tables/symbol_table.txt",
]


def main():
    load_tables = LoadTables()
    load_tables.load_symbol_table(tables[0])

    symbols_table = SymbolTable(load_tables.symbol_table)

    program = read_prog(progs[0])

    prog_index=0
    for instruction in program:
      if instruction.startswith("("):
        symbol = re.sub(r'[\(\)]', "", instruction)
        if not symbols_table.contains(symbol):
          symbols_table.add_entry(symbol, prog_index + 1) 
      prog_index += 1
      
    binary_code = []
    n = 16
    for instruction in program:
      if instruction.startswith("@"):
        symbol = instruction.replace("@", "")
        addr = symbols_table.get_address(symbol)
        if addr:
          binary_code.append(f"0{format((int(addr)), '015b')}")
        else:
          symbols_table.add_entry(symbol, n)
          n+=1 
      else:
        binary_code.append(f"0{format((int('0')), '015b')}")
        
    print(binary_code)

    pass


if __name__ == "__main__":
    print("start")
    main()
