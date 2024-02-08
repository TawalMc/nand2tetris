import re


class Parser:
  
  def __init__(self) -> None:
    self.comp = ""
    self.dest = ""
    self.jump = ""
  
  def display_instruction_parts(self):
    print(f"comp: {self.comp}")
    print(f"dest: {self.dest}")
    print(f"jump: {self.jump}")
  
  def parse(self, line: str):
    instruction = line.split(";")
    
    if (len(instruction) == 2): # dest=cmp;jump or cmp;jump
      self.jump = re.sub(r"\s+", "", instruction[1])
      first_part = instruction[0].split("=")
      if len(first_part) == 2: # dest=cmp;jump
        self.dest = re.sub(r"\s+", "", first_part[0])
        self.comp = re.sub(r"\s+", "", first_part[1])
      else: # cmp;jump
        self.comp = re.sub(r"\s+", "", first_part[0])
        
    elif len(instruction) == 1: # no jump instruction
      first_part = instruction[0].split("=")
      if len(first_part) == 2: # dest=cmp
        self.dest = re.sub(r"\s+", "", first_part[0])
        self.comp = re.sub(r"\s+", "", first_part[1])
      else: # dest=cmp
        self.comp = re.sub(r"\s+", "", first_part[0])
    