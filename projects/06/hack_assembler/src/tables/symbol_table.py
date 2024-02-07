from typing import List, Optional


class SymbolTable:
  def __init__(self, symbols: List[List[str]] = []) -> None:
    self.symbols = symbols # [[R0, 0], [R1, 1], ...]
  
  def add_entry(self, symbol: str, address: int) -> None:
    self.symbols.append([symbol, address])
  
  def contains(self, symbol: str) -> bool:
    for s in self.symbols:
      if symbol == s[0]:
        return True
    return False
  
  def get_address(self, symbol: str) -> Optional[int] :
    for s in self.symbols:
      if symbol == s[0]:
        return s[1]
    return None