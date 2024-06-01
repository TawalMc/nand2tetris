import os
from pathlib import Path
from typing import Optional

from utils.utils import is_valid_file


class SourceHandler:
    def __init__(self, source: str, in_end_with: str, out_end_with: str):
        self.__source = source
        self.__source_files = []
        self.__out_files: Optional[str] = None

        if not self.is_file() and not self.is_dir():
            raise ValueError("argument must be either a file or a folder")

        if self.is_file():
            file_name = os.path.basename(self.__source)
            is_valid_file(file_name, in_end_with, raise_error=True)
            self.__source_files.append(self.__source)

        elif self.is_dir():
            self.__source_files = [
                str(file) for file in Path(self.__source).iterdir() if
                file.is_file() and is_valid_file(str(file), in_end_with)
            ]
            if not self.__source_files:
                raise ValueError("this folder doesn't contain a jack file")

        self.__out_files = [{"in": file, "out": file[: -len(in_end_with)] + f"{out_end_with}"} for file in
                            self.__source_files]

    def is_file(self):
        path = Path(self.__source)
        return path.exists() and path.is_file()

    def is_dir(self):
        path = Path(self.__source)
        return path.exists() and path.is_dir()

    def source_files(self):
        return self.__source_files

    def out_files(self):
        return self.__out_files
