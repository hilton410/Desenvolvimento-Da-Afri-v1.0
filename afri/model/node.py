# ==========================================
# NODE.PY - Árvores AST
# ==========================================
from afri.model.token import Token

class ASTNode:
    def __init__(self, token: Token):
        self._token = token

    def exec(self, **kwargs) -> object:
        return None

    @property
    def token(self) -> Token:
        return self._token

    @property
    def value(self):
        return self._token.value

    def __repr__(self):
        return f"{self._token.value}"

class NumberNode(ASTNode):
    def exec(self, **kwargs) -> object:
        return self.value

class StringNode(ASTNode):
    def exec(self, **kwargs) -> object:
        return self.value

class BooleanNode(ASTNode):
    def exec(self, **kwargs) -> object:
        return self.value

class VariableNode(ASTNode):
    def exec(self, **kwargs) -> object:
        return kwargs['get_variable'](self.value, True)

class AssignNode(ASTNode):
    def __init__(self, left: VariableNode, right: ASTNode):
        super().__init__(Token(Token.EOF, ''))
        self._left: VariableNode = left
        self._right: ASTNode = right

    def exec(self, **kwargs) -> object:
        return kwargs['set_variable'](self.left.value, self.right.exec(**kwargs))

    @property
    def left(self) -> VariableNode:
        return self._left

    @property
    def right(self) -> ASTNode:
        return self._right

    def __repr__(self):
        return f"{self._left} = {self._right}"

class BinOpNode(ASTNode):
    def __init__(self, left: ASTNode, token: Token, right: ASTNode):
        super().__init__(token)
        self._left: ASTNode = left
        self._right: ASTNode = right

    def exec(self, **kwargs) -> object:
        operator = self.token.type
        left = self.left.exec(**kwargs)
        right = self.right.exec(**kwargs)

        if operator == Token.PLUS:
            if isinstance(right, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right

        elif operator == Token.MINUS:
            return left - right

        elif operator == Token.MULTIPLY:
            return left * right

        elif operator == Token.DIViDE:
            if right == 0:
                raise ZeroDivisionError("Erro: Divisão por zero não permitida no afri.")
            return left / right

        return None

    @property
    def left(self) -> ASTNode:
        return self._left

    @property
    def right(self) -> ASTNode:
        return self._right

    def __repr__(self):
        return f"({self._left} {self._token.value} {self._right})"

class VerNode(ASTNode):
    def __init__(self, arg: ASTNode):
        super().__init__(Token(Token.EOF, ''))
        self._arg: ASTNode = arg

    def exec(self, **kwargs) -> object:
        print(self.arg.exec(**kwargs))

    @property
    def arg(self):
        return self._arg

    def __repr__(self):
        return f"ver {self._arg}"

class ReceberNode(ASTNode):
    def __init__(self, var: VariableNode):
        super().__init__(Token(Token.EOF, ''))
        self._var: VariableNode = var

    def exec(self, **kwargs) -> object:
        name = self.var.value
        value = input().strip()

        # Mapeamento dinâmico inteligente no input do afri
        if value == "verdade":
            kwargs['set_variable'](name, True)

        elif value == "falso":
            kwargs['set_variable'](name, False)

        elif value.isdigit():
            kwargs['set_variable'](name, int(value))
        else:
            try:
                kwargs['set_variable'](name, float(value))
            except ValueError:
                kwargs['set_variable'](name, value)

        return kwargs['get_variable'](name, True)

    @property
    def var(self):
        return self._var

    def __repr__(self):
        return f"receber {self._var}"
