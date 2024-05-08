import os
from pathlib import Path
from typing import Optional


class SourceHandler:
    def __init__(self, source: str):
        self.__source = source
        self.source_files = []
        self.out_file: Optional[str] = None

    def is_file(self):
        path = Path(self.__source)
        return path.exists() and path.is_file()

    def is_dir(self):
        path = Path(self.__source)
        return path.exists() and path.is_dir()

    def is_file_valid(self):
        if self.source_files[-1][0].upper() != self.source_files[-1][0]:
            raise ValueError("the file name must start with an uppercase letter")
        if self.source_files[-1][-2:] != "vm":
            raise ValueError("the file extension must be 'vm'")
        return True

    def handle_file(self):
        if self.is_file():
            file_name = os.path.basename(self.__source)
            self.source_files.append(file_name)
            if self.is_file_valid():
                self.out_file = self.__source[: -2] + "asm"
                # continue
        elif self.is_dir():
            # continue
            pass
        pass

    def out_file(self):
        return self.out_file
