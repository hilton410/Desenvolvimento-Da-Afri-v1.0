# ==========================================
# TOKEN.PY - Tokens ou palavras chaves
# ==========================================

class Token:
    # Tipos de dados
    INT = "INTEIRO"
    STRING = "TEXTO"
    FLOAT = "DECIMAL"
    BOOLEAN = "BINARIO"

    # Operadores de atribuição
    ASSIGN = "ATRIBUIR"

    # Operadores matemáticos
    PLUS = "SOMAR"
    MINUS = "SUBTRAIR"
    MULTIPLY = "MULTIPLICAR"
    DIViDE = "DIVIDIR"

    # Identificadores
    ID = "ID"
    EOF = "EOF"

    # Funções
    VER = "VER"
    RECEBER = "RECEBER"

    def __init__(self, tpye: str, value: str | int | float | bool):
        self._type = tpye
        self._value = value

    @property
    def type(self) -> str:
        return self._type

    @property
    def value(self):
        return self._value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"