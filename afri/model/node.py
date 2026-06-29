# ==========================================
# NODE.PY - Árvores AST
# ==========================================
from afri.model.token import Token

class ASTNode:
    def __init__(self, token: Token):
        self._token = token

    @property
    def token(self):
        return self._token

    @property
    def value(self):
        return self._token.value

    def __repr__(self):
        return f"{self._token.value}"

class NumberNode(ASTNode): pass
class StringNode(ASTNode): pass
class BooleanNode(ASTNode): pass
class VariableNode(ASTNode): pass

class BinOpNode(ASTNode):
    def __init__(self, left: ASTNode, token: Token, right: ASTNode):
        super().__init__(token)
        self._left: ASTNode = left
        self._right: ASTNode = right

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    def __repr__(self):
        return f"({self._left} {self._token.value} {self._right})"

class AssignNode(ASTNode):
    def __init__(self, left: VariableNode, right: ASTNode):
        super().__init__(Token(Token.EOF, ''))
        self._left: VariableNode = left
        self._right: ASTNode = right

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    def __repr__(self):
        return f"{self._left} = {self._right}"

class VerNode(ASTNode):
    def __init__(self, arg: ASTNode):
        super().__init__(Token(Token.EOF, ''))
        self._arg: ASTNode = arg

    @property
    def arg(self):
        return self._arg

    def __repr__(self): return f"ver {self._arg}"

class ReceberNode(ASTNode):
    def __init__(self, var: VariableNode):
        super().__init__(Token(Token.EOF, ''))
        self._var: VariableNode = var

    @property
    def var(self):
        return self._var

    def __repr__(self): return f"receber {self._var}"
