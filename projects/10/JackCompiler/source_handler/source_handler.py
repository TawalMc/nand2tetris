import os
from pathlib import Path
from typing import Optional


def is_valid_jack_file(file: str, raise_error=False):
    if not raise_error:
        return file[0].upper() == file[0] and file.endswith(".jack")

    if file[0].upper() != file[0]:
        raise ValueError("the file name must start with an uppercase letter")
    if not file.endswith(".jack"):
        raise ValueError("the file extension must be 'jack'")


class SourceHandler:
    def __init__(self, source: str, tokenization=False):
        self.__source = source
        self.__source_files = []
        self.__out_files: Optional[str] = None
        self.__tokenization = tokenization

        if not self.is_file() and not self.is_dir():
            raise ValueError("argument must be either a file or a folder")

        tail = "OwnT" if self.__tokenization else "OwnP"
        if self.is_file():
            file_name = os.path.basename(self.__source)
            is_valid_jack_file(file_name, raise_error=True)
            self.__source_files.append(self.__source)

        elif self.is_dir():
            self.__source_files = [
                str(file) for file in Path(self.__source).iterdir() if file.is_file() and is_valid_jack_file(str(file))
            ]
            if not self.__source_files:
                raise ValueError("this folder doesn't contain a jack file")

            # self.__out_files = f"{Path(self.__source).resolve()}/{os.path.basename(self.__source)}{tail}.xml"
        self.__out_files = [{"in": file, "out": file[: -5] + f"{tail}.xml"} for file in self.__source_files]

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
