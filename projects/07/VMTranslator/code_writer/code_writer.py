from constants import arithmetic_instructions


class CodeWriter:
    def __init__(self, file_path: str):
        self.__count_ari_inst = 0
        self.__file = open(file_path, 'w+')

    def write_arithmetic(self, command):
        instructions = arithmetic_instructions(command, self.__count_ari_inst)
        for inst in instructions:
            self.__file.write(f"{inst}\n")
        self.__count_ari_inst += 1

    def write_push_pop(self):
        pass

    def close(self):
        self.__file.close()
