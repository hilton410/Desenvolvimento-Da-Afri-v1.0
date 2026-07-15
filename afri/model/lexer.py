# ==========================================
# LEXER.PY - Gerador de tokens
# ==========================================
from .token import Token

class Lexer:
    def __init__(self, code: str):
        self._index = 0

        self._code = code
        self._character = code[0] if code else ''

    def _getline(self):
        lines = self._code[:self._index].split('\n')
        return len(lines), len(lines[-1]) + 1

    def _advance(self):
        self._index += 1
        if self._index < len(self._code):
            self._character = self._code[self._index]
        else:
            self._index = len(self._code)
            self._character = ''
            return False
        return True

    def _retreat(self):
        self._index -= 1
        if self._index >= 0:
            self._character = self._code[self._index]
        else:
            self._index = 0
            self._character = ''
            return False
        return True

    def _skip_whitespace(self):
        while self._character and self._character.isspace():
            self._advance()

    def _number(self):
        result = ''
        line = self._getline()
        while self._character and self._character.isdigit():
            result += self._character
            self._advance()

        if self._character == '.' or self._character == 'e':
            if self._character != 'e':
                result += self._character
                self._advance()
                while self._character and self._character.isdigit():
                    result += self._character
                    self._advance()

            character = self._character
            self._advance()
            character += self._character
            self._advance()

            if len(character) == 2:
                if character[0] == 'e' and (character[1] in ['+', '-'] or character[1].isdigit()):
                    while self._character and self._character.isdigit():
                        character += self._character
                        self._advance()

                    if character[-1].isdigit():
                        result += character
                    else:
                        for c in range(len(character)):
                            self._retreat()
                else:
                    for c in range(len(character)):
                        self._retreat()
            else:
                self._retreat()

            return Token(Token.FLOAT, float(result), line)

        if result:
            return Token(Token.INTEGER, int(result), line)
        return Token(Token.EOF, '', line)

    def _string(self):
        result = ''
        line = self._getline()
        token = Token.FAT_STRING
        self._advance()
        while self._character:
            if self._character == '\\':
                if not self._advance():
                    continue

                match self._character:
                    case 'n': result += '\n'
                    case 't': result += '\t'
                    case _: result += self._character
                self._advance()

            elif self._character == '"':
                token = Token.STRING
                self._advance()
                break
            else:
                result += self._character
                self._advance()

        return Token(token, result, line)

    def _comment(self):
        self._advance()
        while self._character and self._character != '#':
            self._advance()
        self._advance()

    def identifier(self):
        result = ''
        line = self._getline()
        while self._character and (self._character.isalnum() or self._character == '_'):
            result += self._character
            self._advance()

        if token_type := Token.get_type(result):
            return Token(token_type, result, line)
        return Token(Token.ID, result, line)

    def next(self):
        while self._character:
            line = self._getline()
            character = self._character
            if self._character.isspace():
                self._skip_whitespace()
                continue

            if self._character.isdigit():
                return self._number()

            if self._character == '"':
                return self._string()

            if self._character == '#':
                self._comment()
                continue

            if self._character == "_" or self._character.isalpha():
                return self.identifier()

            listch = []
            for _ in range(Token.char_max()):
                listch.append(character)
                if self._advance():
                    character +=  self._character
                else:
                    break

            for _ in range(len(listch)):
                self._retreat()

            for ch in listch[::-1]:
                if token_type := Token.get_type(ch):
                    for _ in range(len(ch)): self._advance()
                    return Token(token_type, ch, line)
            return Token(Token.EOF, listch[0], line)
        return Token(Token.EOF, '', self._getline())
