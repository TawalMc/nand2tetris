from tokenizer.lexical_elements import SYMBOLS, KEYWORDS, KEYWORD, STRING_CONST, INT_CONST, IDENTIFIER, SYMBOL


class Tokenizer:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.__current_line = ""
        self.__line_content = []
        self.__current_token = ""

        self.file = open(file_path, 'r')

    def get_current_token(self):
        return self.__current_token

    def get_current_line(self):
        return self.__current_line

    def get_line_content(self):
        return self.__line_content

    def has_more_lines(self) -> bool:
        curr_pos = self.file.tell()
        has_it = bool(self.file.readline())
        self.file.seek(curr_pos)

        return has_it

    def read_line(self):
        self.purge_comments_from_line()
        self.__line_content = [c for c in self.__current_line] if len(self.__current_line) >= 1 else []

    # TODO: rewrite the logic of this function
    def has_more_tokens(self):
        return bool(self.__line_content)

    def advance(self):
        self.__current_token = ""
        content = self.__line_content
        for (index, item) in enumerate(content):
            # handle string case: "..."
            if item == '"':
                try:
                    second_dquote_index = content.index('"', index + 1)
                    self.__current_token = ''.join(str(c) for c in content[index:second_dquote_index + 1])
                    self.__line_content = content[second_dquote_index + 1:]
                    break
                except ValueError:
                    pass

            # skip if space or \n
            if item.isspace() or item == "\n":
                self.__line_content = content[index + 1:]
                break

            self.__current_token += item

            # if symbol just keep it and advance
            if self.__is_char_symbol(item):
                self.__line_content = content[index + 1:]
                break

            # start of new token
            if index + 1 < len(content) and self.__is_char_symbol(content[index + 1]):
                self.__line_content = content[index + 1:]
                break

    def token_type(self):
        return self.token_info()[1]

    # write a regex to check if token is identifier
    def token_info(self):
        if self.__current_token in KEYWORDS:
            return KEYWORD, self.__current_token
        if self.__current_token in SYMBOLS:
            return SYMBOL, self.symbol()
        if self.__current_token.startswith('"') and self.__current_token.endswith('"'):
            return STRING_CONST, self.string_val()
        try:
            int(self.__current_token)
            return INT_CONST, self.int_val()
        except ValueError:
            pass

        try:
            int(self.__current_token[0])
            raise ValueError("Invalid token")
        except ValueError:
            return IDENTIFIER, self.identifier()

    def keyword(self):
        return self.__current_token

    def symbol(self):
        return self.__current_token[0]

    def identifier(self):
        return self.__current_token

    def int_val(self):
        return int(self.__current_token)

    def string_val(self):
        return self.__current_token[1:-1]

    @staticmethod
    def __is_char_symbol(c: str) -> bool:
        return c in SYMBOLS

    def purge_comments_from_line(self):
        self.__current_line = self.file.readline()

        if self.__current_line.find("/*") >= 0:
            content = self.__current_line
            while content and content.find("*/") < 0:
                content = self.file.readline()
            self.purge_comments_from_line()

        if self.__current_line.isspace() or self.__current_line == "\n":
            self.purge_comments_from_line()

        eol_comment_index = self.__current_line.find("//")
        if eol_comment_index >= 0:
            self.__current_line = self.__current_line[: eol_comment_index]

    def close(self):
        self.file.close()
