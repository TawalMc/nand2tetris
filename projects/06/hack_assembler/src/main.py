from src.tables.table import LoadTables
from src.utils.utils import read_prog


def main():
    prog = read_prog("../../../04/fill/Fill.asm")
    table = LoadTables()
    table.load_symbol_table("./tables/symbol_table.txt")
    print(table.symbol_table)
    pass


if __name__ == "__main__":
    print("ssssssssssssss")
    main()
