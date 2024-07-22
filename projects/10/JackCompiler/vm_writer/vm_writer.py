class VMWriter:
    def __init__(self, out_put_file: str):
        self.__out_file = open(out_put_file, 'w+')

    def write_push(self, segment: str, index: int):
        self.__out_file.write(f"push {segment} {index}\n")

    def write_pop(self, segment: str, index: int):
        self.__out_file.write(f"pop {segment} {index}\n")

    def write_arithmetic(self, command: str):
        self.__out_file.write(f"{command}\n")

    def write_label(self, label: str):
        self.__out_file.write(f"label {label}\n")

    def write_goto(self, label: str):
        self.__out_file.write(f"goto {label}\n")

    def write_if(self, label: str):
        self.__out_file.write(f"if-goto {label}\n")

    def write_call(self, name: str, nb_args: int):
        self.__out_file.write(f"call f{name} {nb_args}\n")

    def write_function(self, name: str, nb_locals: int):
        self.__out_file.write(f"function {name} {nb_locals if nb_locals > 0 else ''}\n")

    def write_return(self):
        self.__out_file.write("return \n")

    def close(self):
        self.__out_file.close()
