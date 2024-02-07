import re
from typing import List


class LoadTables:
    def __init__(self) -> None:
        self.symbol_table = []
        self.dest_table = []
        self.jump_table = []
        self.comp_table = []

    def load_table(self, path: str, columns: int) -> List[List[str]]:
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
        self.symbol_table = self.load_table(path, 2)
