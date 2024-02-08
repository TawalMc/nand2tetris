import re
from tables import LoadTables, SymbolTable
from hparser import Parser
from utils import read_prog

progs = [
    "/home/tawaliou/Documents/apps/nand2tetris/projects/04/fill/Fill.asm",
]

tables = [
    "/home/tawaliou/Documents/apps/nand2tetris/projects/06/hack_assembler/src/tables/symbol_table.txt",
    "/home/tawaliou/Documents/apps/nand2tetris/projects/06/hack_assembler/src/tables/comp_table.txt",
    "/home/tawaliou/Documents/apps/nand2tetris/projects/06/hack_assembler/src/tables/dest_table.txt",
    "/home/tawaliou/Documents/apps/nand2tetris/projects/06/hack_assembler/src/tables/jump_table.txt",
]


def main():
    load_tables = LoadTables(symbol_path=tables[0], 
                             comp_path=tables[1],
                             dest_path=tables[2],
                             jump_path=tables[3]
                             )
    
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
      if not instruction.startswith("("):
          if instruction.startswith("@"):
            symbol = instruction.replace("@", "")
            addr = symbols_table.get_address(symbol)
            if addr:
              binary_code.append(f"0{format((int(addr)), '015b')}")
            else:
              symbols_table.add_entry(symbol, n)
              binary_code.append(f"0{format((int(n)), '015b')}")
              n+=1 
          else:
            parser = Parser()
            parser.parse(instruction)
            parser.display_instruction_parts()
            binary_code.append(f"0{format((int('0')), '015b')}")
        
    # print(binary_code)

    pass


if __name__ == "__main__":
    print("start")
    main()
