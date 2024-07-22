from tokenizer.lexical_elements import Kind


class SymbolTable:
    def __init__(self):
        self.__symbol_table = dict()
        self.__table_name = ""
        self.__kind_count = {Kind.STATIC: 0, Kind.ARG: 0, Kind.FIELD: 0, Kind.LOCAL: 0}

    def reset(self):
        self.__symbol_table = dict()
        self.__table_name = ""
        self.__kind_count = {Kind.STATIC: 0, Kind.ARG: 0, Kind.FIELD: 0, Kind.LOCAL: 0}

    def define(self, name: str, type: str, kind: str):
        new_name = {"type": type, "kind": kind, "index": self.__kind_count[kind]}
        self.__symbol_table[name] = new_name
        self.__kind_count[kind] += 1
        return new_name

    def var_count(self, kind: str):
        return self.__kind_count[kind]

    def kind_of(self, name: str):
        return None if name not in self.__symbol_table else self.__symbol_table[name]['kind']

    def type_of(self, name: str):
        return None if name not in self.__symbol_table else self.__symbol_table[name]['type']

    def index_of(self, name: str):
        return None if name not in self.__symbol_table else self.__symbol_table[name]['index']

    def update_symbol_table_name(self, table_name: str):
        self.__table_name = table_name

    def is_key(self, key: str):
        return bool(key in self.__symbol_table)

    def table_name(self):
        return self.__table_name
