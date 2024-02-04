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
            c = 0
            matching = []
            for l in _line:
                if c < columns:
                    matching.append(re.sub(r"\s+", "", l))
                table.append(matching)
                c += 1
        file.close()
        return table

    def load_symbol_table(self, path: str):
        self.symbol_table = self.load_table(path, 2)
