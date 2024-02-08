import re
from typing import List


class LoadTables:
    def __init__(self, 
                 symbol_path: str = None,
                 comp_path: str = None,
                 dest_path: str = None,
                 jump_path: str = None,
                 ) -> None:
        self.symbol_table = [] if not symbol_path else self.load_table(symbol_path)
        self.dest_table = [] if not dest_path else self.load_table(dest_path)
        self.jump_table = [] if not jump_path else self.load_table(jump_path)
        self.comp_table = [] if not comp_path else self.load_table(comp_path)
        
    def display_tables(self):
      print(f"symbol_table: {self.symbol_table}")
      print(f"comp_table: {self.comp_table}")
      print(f"dest_table: {self.dest_table}")
      print(f"jump_table: {self.jump_table}")
  
    def load_table(self, path: str) -> List[List[str]]:
        file = open(path, 'r')
        table = []
        for line in file:
            _line = line.split(" ")
            matching = []
            for l in _line:
              matching.append(re.sub(r"\s+", "", l))
            table.append(matching)
        file.close()
        return table

    def load_symbol_table(self, path: str) -> None :
        self.symbol_table = self.load_table(path)

    def load_comp_table(self, path: str) -> None :
        self.comp_table = self.load_table(path)
        
    def load_dest_table(self, path: str) -> None :
        self.dest_table = self.load_table(path)
    
    def load_dest_table(self, path: str) -> None :
        self.jump_table = self.load_table(path)