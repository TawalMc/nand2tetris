class Parser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.current_command = None

        self.file = open(file_path, 'r')

    def has_more_lines(self) -> bool:
        curr_pos = self.file.tell()
        has_it = bool(self.file.readline())
        self.file.seek(curr_pos)

        return has_it

    def advance(self):
        self.current_command = self.file.readline()
