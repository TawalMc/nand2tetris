from typing import List, Optional


class Code:
  def __init__(self, dest_table: List[List[str]], cmp_table: List[List[str]], jump_table: List[List[str]]) -> None:
    self.dest_table = dest_table
    self.cmp_table = cmp_table
    self.jump_table = jump_table
    
  def dest(self, instruction: str):
    line = self.get_elt(instruction, self.dest_table)
    return line[1] 
    
  def cmp(self, instruction: str):
    line = self.get_elt(instruction, self.cmp_table)
    return f"{line[2]}{line[1]}" 
  
  def jump(self, instruction: str):
    line = self.get_elt(instruction, self.jump_table)
    return line[1] 
  
  def binary_code(self, dest_inst: str, cmp_inst: str, jump_inst: str):
    return f"111{self.cmp(cmp_inst)}{self.dest(dest_inst)}{self.jump(jump_inst)}"
    
  def get_elt(self, inst: str, table: List[List[str]]) -> Optional[int] :
   if not len(inst):
     return table[0]
   
   for line in table:
     if inst == line[0]:
      return line
   return table[0]
  