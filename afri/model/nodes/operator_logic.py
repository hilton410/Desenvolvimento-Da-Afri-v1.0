# =======================================================
# OPERATOR_LOGIC.PY - Arvóres AST para operadores lógicos
# =======================================================
from . import Token, ASTNode, BinOpNode, UniOpNode

class LessNode(BinOpNode):
    FEATURE = {
        'token': Token.LESS_THAN,
        'type': Token.OPERATOR,
        'order': 4,
        'fat': True,
    }

    @ASTNode.ctrl
    def exec(self, **kwargs):
        left = self.left.exec(**kwargs)
        right = self.right.exec(**kwargs)
        union = int | float | bool

        if ((
            (not isinstance(left, union) or not isinstance(right, union)) and
            (not isinstance(left, str) and not isinstance(right, str))
        ) or (
            (not isinstance(right, union) or not isinstance(left, union)) and
            (isinstance(right, str) and not isinstance(left, str))
        )):
            ASTNode.add_ctrl(Token.ERROR, [
                Token.VALUEERROR, self.getline(),
                f'{ASTNode.format_data(left, src=True)} {Token.token(Token.LESS_THAN)} '
                f'{ASTNode.format_data(right, src=True)} são incompatíveis'
            ])
            return None

        if isinstance(left, str) or isinstance(right, str):
            left = ASTNode.format_data(left)
            right = ASTNode.format_data(right)

        return left < right

    @property
    def center(self) -> bool:
        return True

class LessEqualNone(BinOpNode):
    FEATURE = {
        'token': Token.LESS_EQUAL,
        'type': Token.OPERATOR,
        'order': 4,
        'fat': True,
    }

    @ASTNode.ctrl
    def exec(self, **kwargs):
        left = self.left.exec(**kwargs)
        right = self.right.exec(**kwargs)
        union = int | float | bool

        if ((
            (not isinstance(left, union) or not isinstance(right, union)) and
            (not isinstance(left, str) and not isinstance(right, str))
        ) or (
            (not isinstance(right, union) or not isinstance(left, union)) and
            (isinstance(right, str) and not isinstance(left, str))
        )):
            ASTNode.add_ctrl(Token.ERROR, [
                Token.VALUEERROR, self.getline(),
                f'{ASTNode.format_data(left, src=True)} {Token.token(Token.LESS_EQUAL)} '
                f'{ASTNode.format_data(right, src=True)} são incompatíveis'
            ])
            return None

        if isinstance(left, str) or isinstance(right, str):
            left = ASTNode.format_data(left)
            right = ASTNode.format_data(right)

        return left <= right

    @property
    def center(self) -> bool:
        return True

class GreatNode(BinOpNode):
    FEATURE = {
        'token': Token.GREAT_THAN,
        'type': Token.OPERATOR,
        'order': 4,
        'fat': True
    }

    @ASTNode.ctrl
    def exec(self, **kwargs):
        left = self.left.exec(**kwargs)
        right = self.right.exec(**kwargs)
        union = int | float | bool

        if ((
            (not isinstance(left, union) or not isinstance(right, union)) and
            (not isinstance(left, str) and not isinstance(right, str))
        ) or (
            (not isinstance(right, union) or not isinstance(left, union)) and
            (isinstance(right, str) and not isinstance(left, str))
        )):
            ASTNode.add_ctrl(Token.ERROR, [
                Token.VALUEERROR, self.getline(),
                f'{ASTNode.format_data(left, src=True)} {Token.token(Token.GREAT_THAN)} '
                f'{ASTNode.format_data(right, src=True)} são incompatíveis'
            ])
            return None

        if isinstance(left, str) or isinstance(right, str):
            left = ASTNode.format_data(left)
            right = ASTNode.format_data(right)

        return left > right

    @property
    def center(self) -> bool:
        return True

class GreatEqualNone(BinOpNode):
    FEATURE = {
        'token': Token.GREAT_EQUAL,
        'type': Token.OPERATOR,
        'order': 4,
        'fat': True,
    }

    @ASTNode.ctrl
    def exec(self, **kwargs):
        left = self.left.exec(**kwargs)
        right = self.right.exec(**kwargs)
        union = int | float | bool

        if ((
            (not isinstance(left, union) or not isinstance(right, union)) and
            (not isinstance(left, str) and not isinstance(right, str))
        ) or (
            (not isinstance(right, union) or not isinstance(left, union)) and
            (isinstance(right, str) and not isinstance(left, str))
        )):
            ASTNode.add_ctrl(Token.ERROR, [
                Token.VALUEERROR, self.getline(),
                f'{ASTNode.format_data(left, src=True)} {Token.token(Token.GREAT_EQUAL)} '
                f'{ASTNode.format_data(right, src=True)} são incompatíveis'
            ])
            return None

        if isinstance(left, str) or isinstance(right, str):
            left = ASTNode.format_data(left)
            right = ASTNode.format_data(right)

        return left >= right

    @property
    def center(self) -> bool:
        return True

class EqualNode(BinOpNode):
    FEATURE = {
        'token': Token.EQUAL,
        'type': Token.OPERATOR,
        'order': 5,
        'fat': True
    }

    @ASTNode.ctrl
    def exec(self, **kwargs):
        left = self.left.exec(**kwargs)
        right = self.right.exec(**kwargs)
        if ASTNode.exs_ctrl(): return None

        return left == right

    @property
    def center(self) -> bool:
        return True

class NoEqualNode(BinOpNode):
    FEATURE = {
        'token': Token.NO_EQUAL,
        'type': Token.OPERATOR,
        'order': 5,
        'fat': True
    }

    @ASTNode.ctrl
    def exec(self, **kwargs):
        left = self.left.exec(**kwargs)
        right = self.right.exec(**kwargs)
        if ASTNode.exs_ctrl(): return None

        return left != right

    @property
    def center(self) -> bool:
        return True

class AndNode(BinOpNode):
    FEATURE = {
        'token': Token.AND,
        'type': Token.OPERATOR,
        'order': 6,
        'fat': True
    }

    @ASTNode.ctrl
    def exec(self, **kwargs):
        left = self.left.exec(**kwargs)
        right = self.right.exec(**kwargs)
        if ASTNode.exs_ctrl(): return None

        return left and right

    @property
    def center(self) -> bool:
        return True

class OrNode(BinOpNode):
    FEATURE = {
        'token': Token.OR,
        'type': Token.OPERATOR,
        'order': 6,
        'fat': True
    }

    @ASTNode.ctrl
    def exec(self, **kwargs):
        left = self.left.exec(**kwargs)
        right = self.right.exec(**kwargs)
        if ASTNode.exs_ctrl(): return None

        return left or right

    @property
    def center(self) -> bool:
        return True

class NotNode(UniOpNode):
    FEATURE = {
        'token': Token.NOT,
        'type': Token.OPERATOR,
        'order': 6,
        'uni': True,
    }

    @ASTNode.ctrl
    def exec(self, **kwargs):
        right = self.right.exec(**kwargs)
        if ASTNode.exs_ctrl(): return None

        return not right