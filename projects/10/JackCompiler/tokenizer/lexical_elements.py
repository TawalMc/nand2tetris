# CONSTANTS
KEYWORDS = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void',
            'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']

SYMBOLS = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']

KEYWORD = "KEYWORD"
SYMBOL = "SYMBOL"
IDENTIFIER = "IDENTIFIER"
INT_CONST = "INT_CONST"
STRING_CONST = "STRING_CONST"

TOKEN_XML = {
    "KEYWORD": "keyword",
    "SYMBOL": "symbol",
    "IDENTIFIER": "identifier",
    "INT_CONST": "integerConstant",
    "STRING_CONST": "stringConstant"
}

TOKEN_TYPES = [
    "keyword",
    "symbol",
    "identifier",
    "integerConstant",
    "stringConstant"
]


class Kind:
    STATIC = "static"
    FIELD = "field"
    ARG = "arg"
    VAR = "var"
    ROUTINE = "subroutine"
    CLASS = "class"
    LOCAL = "local"


class IdentifierStatus:
    DEFINED = 'defined'
    USED = "used"
