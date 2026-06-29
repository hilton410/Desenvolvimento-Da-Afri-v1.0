# ==========================================
# LEXER.PY - Gerador de tokens
# ==========================================
from afri.model.token import Token

class Lexer:
    def __init__(self, code: str):
        self._index = 0
        self._code = code
        self._character = code[0] if code else None

    def _advance(self):
        self._index += 1
        if self._index < len(self._code):
            self._character = self._code[self._index]
        else:
            self._character = None
            return False
        return True

    def _skip_whitespace(self):
        while self._character is not None and self._character.isspace():
            self._advance()

    def _number(self):
        result = ''
        while self._character is not None and self._character.isdigit():
            result += self._character
            self._advance()

        if self._character == '.':
            result += self._character
            self._advance()
            while self._character is not None and self._character.isdigit():
                result += self._character
                self._advance()
            return Token(Token.FLOAT, float(result))

        if result:
            return Token(Token.INT, int(result))
        return Token(Token.EOF, '')

    def _string(self):
        result = ''
        self._advance()
        while self._character is not None:
            if self._character == '\\':
                result += self._character
                if not self._advance():
                    return Token(Token.EOF, '')
            
            elif self._character == '"' or self._character == '\n':
                break
            
            result += self._character
            self._advance()
            
        if self._character == '"':
            self._advance()
            return Token(Token.STRING, result)
        else:
            raise SyntaxError("Erro Léxico: String não fechada com aspas.")

    def identifier(self):
        result = ''
        while self._character is not None and (self._character.isalnum() or self._character == '_'):
            result += self._character
            self._advance()

        if result == 'ver':
            return Token(Token.VER, result)
        if result == 'receber':
            return Token(Token.RECEBER, result)

        if result in ("verdade", "falso"):
            return Token(Token.BOOLEAN, result)

        return Token(Token.ID, result)

    def next(self) -> Token:
        while self._character is not None:
            if self._character.isspace():
                self._skip_whitespace()
                continue
            
            if self._character.isdigit():
                return self._number()
            
            if self._character == '"':
                return self._string()
            
            if self._character == "_" or self._character.isalpha():
                return self.identifier()

            if self._character == '=':
                self._advance()
                return Token(Token.ASSIGN, '=')
            if self._character == '+':
                self._advance()
                return Token(Token.PLUS, '+')
            if self._character == '-':
                self._advance()
                return Token(Token.MINUS, '-')
            if self._character == '*':
                self._advance()
                return Token(Token.MULTIPLY, '*')
            if self._character == '/':
                self._advance()
                return Token(Token.DIViDE, '/')

            raise SyntaxError(f"Caractere inválido: '{self._character}'")

        return Token(Token.EOF, '')