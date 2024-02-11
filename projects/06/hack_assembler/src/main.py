import re
import sys
from tables import LoadTables, SymbolTable
from hparser import Parser
from hcode import Code
from utils import read_prog, represents_int
import os

def get_file_full_path(relative_path: str) -> str:
  absolute_path = os.path.dirname(__file__)
  return os.path.join(absolute_path, relative_path)

tables = [
    get_file_full_path("tables/symbol_table.txt"),
    get_file_full_path("tables/comp_table.txt"),
    get_file_full_path("tables/dest_table.txt"),
    get_file_full_path("tables/jump_table.txt"),
]

def main():
    in_file = sys.argv[1]
    out_file = sys.argv[2]
  
    load_tables = LoadTables(symbol_path=tables[0], 
                             comp_path=tables[1],
                             dest_path=tables[2],
                             jump_path=tables[3]
                             )
    
    symbols_table = SymbolTable(load_tables.symbol_table)
    
    code = Code(load_tables.dest_table, load_tables.comp_table, load_tables.jump_table)

    program = read_prog(in_file)
    # print(program)
    prog_index=0
    for instruction in program:
      if instruction.startswith("("):
        prog_index -= 1 
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
            if represents_int(symbol):
              addr = int(symbol)
            else:
              addr = symbols_table.get_address(symbol)
        
              if not addr:
               addr = n
               symbols_table.add_entry(symbol, n)
               n+=1
               
            binary_code.append(f"{format((int(addr)), '016b')}") 
          else:
            parser = Parser()
            parser.parse(instruction)
            binary_code.append(code.binary_code(parser.dest, parser.comp, parser.jump))
    
    # print(symbols_table.symbols)
    # with open(out_file, "w+") as writer:
    #   for b in binary_code:    
    #     writer.write(f"{b}\n")



if __name__ == "__main__":
    print("start")
    main()
