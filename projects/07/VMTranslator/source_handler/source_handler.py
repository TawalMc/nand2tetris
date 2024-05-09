import os
from pathlib import Path
from typing import Optional


def is_valid_vm_file(file: str, raise_error=False):
    if not raise_error:
        return file[0].upper() == file[0] and file.endswith(".vm")

    if file[0].upper() != file[0]:
        raise ValueError("the file name must start with an uppercase letter")
    if not file.endswith(".vm"):
        raise ValueError("the file extension must be 'vm'")


class SourceHandler:
    def __init__(self, source: str):
        self.__source = source
        self.__source_files = []
        self.__out_file: Optional[str] = None

        if not self.is_file() and not self.is_dir():
            raise ValueError("argument must be either a file or a folder")

        if self.is_file():
            file_name = os.path.basename(self.__source)
            is_valid_vm_file(file_name, raise_error=True)
            self.__source_files.append(self.__source)
            self.__out_file = self.__source[: -2] + "asm"

        elif self.is_dir():
            self.__source_files = [
                str(file) for file in Path(self.__source).iterdir() if file.is_file() and is_valid_vm_file(str(file))
            ]
            if not self.__source_files:
                raise ValueError("this folder doesn't contain a vm file")
            self.__out_file = f"{Path(self.__source).resolve()}/{os.path.basename(self.__source)}.asm"

    def is_file(self):
        path = Path(self.__source)
        return path.exists() and path.is_file()

    def is_dir(self):
        path = Path(self.__source)
        return path.exists() and path.is_dir()

    def source_files(self):
        return self.__source_files

    def out_file(self):
        return self.__out_file
