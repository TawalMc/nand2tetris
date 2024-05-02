from typing import Optional

from constants import commands, C_ARITHMETIC


class Parser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.current_command = ""

        self.file = open(file_path, 'r')

    def has_more_lines(self) -> bool:
        curr_pos = self.file.tell()
        has_it = bool(self.file.readline())
        self.file.seek(curr_pos)

        return has_it

    def advance(self):
        self.current_command = self.file.readline()

    def command_type(self) -> Optional[str]:
        cmd_start = self.current_command.split()[0] if self.current_command.split() else None
        return commands.get(cmd_start, None)

    def command(self) -> Optional[str]:
        return self.current_command.split()[0] if self.current_command.split() else None

    def arg1(self) -> str:
        if self.command_type() == C_ARITHMETIC:
            return self.current_command.split()[0]
        return self.current_command.split()[1]

    def arg2(self) -> str:
        return self.current_command.split()[2] if len(self.current_command.split()) > 2 else None

    def close(self):
        self.file.close()
