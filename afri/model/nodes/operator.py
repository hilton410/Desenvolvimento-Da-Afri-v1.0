# ==================================================
# OPERATOR.PY - Arvóres AST para operadores
# ==================================================
from . import Token, ASTNode, BinOpNode

class PlusNode(BinOpNode):
    FEATURE = {
        'token': Token.PLUS,
        'type': Token.OPERATOR,
        'order': 1
    }

    @ASTNode.ctrl
    def exec(self, **kwargs):
        left = self.left.exec(**kwargs)
        right = self.right.exec(**kwargs)
        union = int | float | bool | str
        if ASTNode.exs_ctrl(): return None

        if ((
            (left is None and not isinstance(right, str)) or
            (isinstance(left, int | float) and not isinstance(right, union)) or
            (isinstance(left, bool) and not isinstance(right, union)) or
            (not isinstance(left, None | union) and not isinstance(right, str))
        ) or (
            (right is None and not isinstance(left, str)) or
            (isinstance(right, int | float) and not isinstance(left, union)) or
            (isinstance(right, bool) and not isinstance(left, union)) or
            (not isinstance(left, None | union) and not isinstance(right, str))
        )):
            ASTNode.add_ctrl(Token.ERROR, [
                Token.VALUEERROR, self.getline(),
                f'{ASTNode.format_data(left, src=True)} {Token.token(Token.PLUS)} '
                f'{ASTNode.format_data(right, src=True)} são incompatíveis'
            ])
            return None

        if isinstance(left, str) or isinstance(right, str):
            left = ASTNode.format_data(left)
            right = ASTNode.format_data(right)

        return left + right

class MinusNode(BinOpNode):
    FEATURE = {
        'token': Token.MINUS,
        'type': Token.OPERATOR,
        'order': 1
    }

    @ASTNode.ctrl
    def exec(self, **kwargs):
        left = self.left.exec(**kwargs)
        right = self.right.exec(**kwargs)
        if ASTNode.exs_ctrl(): return None

        if not isinstance(left, int | float | bool) or not isinstance(right, int | float | bool):
            ASTNode.add_ctrl(Token.ERROR, [
                Token.VALUEERROR, self.getline(),
                f'{ASTNode.format_data(left, src=True)} {Token.token(Token.MINUS)} '
                f'{ASTNode.format_data(right, src=True)} são incompatíveis'
            ])
            return None

        return left - right

class MultiplyNode(BinOpNode):
    FEATURE = {
        'token': Token.MULTIPLY,
        'type': Token.OPERATOR,
        'order': 2
    }

    @ASTNode.ctrl
    def exec(self, **kwargs):
        left = self.left.exec(**kwargs)
        right = self.right.exec(**kwargs)
        if ASTNode.exs_ctrl(): return None

        if not isinstance(left, int | float | bool) or not isinstance(right, int | float | bool):
            ASTNode.add_ctrl(Token.ERROR, [
                Token.VALUEERROR, self.getline(),
                f'{ASTNode.format_data(left, src=True)} {Token.token(Token.MULTIPLY)} '
                f'{ASTNode.format_data(right, src=True)} são incompatíveis'
            ])
            return None

        return left * right

class DivideNode(BinOpNode):
    FEATURE = {
        'token': Token.DIVIDE,
        'type': Token.OPERATOR,
        'order': 2
    }

    @ASTNode.ctrl
    def exec(self, **kwargs):
        left = self.left.exec(**kwargs)
        right = self.right.exec(**kwargs)
        if ASTNode.exs_ctrl(): return None

        if not isinstance(left, int | float | bool) or not isinstance(right, int | float | bool):
            ASTNode.add_ctrl(Token.ERROR, [
                Token.VALUEERROR, self.getline(),
                f'{ASTNode.format_data(left, src=True)} {Token.token(Token.DIVIDE)} '
                f'{ASTNode.format_data(right, src=True)} são incompatíveis'
            ])
            return None

        if right == 0:
            ASTNode.add_ctrl(Token.ERROR, [
                Token.VALUEERROR, self.getline(),
                f'{ASTNode.format_data(left, src=True)} {Token.token(Token.DIVIDE)} '
                f'{ASTNode.format_data(right, src=True)} erro de divisão por zero'
            ])
        else:
            return left / right
        return None

class ModuleNode(BinOpNode):
    FEATURE = {
        'token': Token.MODULE,
        'type': Token.OPERATOR,
        'order': 2
    }

    @ASTNode.ctrl
    def exec(self, **kwargs):
        left = self.left.exec(**kwargs)
        right = self.right.exec(**kwargs)
        if ASTNode.exs_ctrl(): return None

        if not isinstance(left, int | float | bool) or not isinstance(right, int | float | bool):
            ASTNode.add_ctrl(Token.ERROR, [
                Token.VALUEERROR, self.getline(),
                f'{ASTNode.format_data(left, src=True)} {Token.token(Token.MODULE)} '
                f'{ASTNode.format_data(right, src=True)} são incompatíveis'
            ])
            return None

        return left % right

class PowNode(BinOpNode):
    FEATURE = {
        'token': Token.POW,
        'type': Token.OPERATOR,
        'order': 3
    }

    @ASTNode.ctrl
    def exec(self, **kwargs):
        left = self.left.exec(**kwargs)
        right = self.right.exec(**kwargs)
        if ASTNode.exs_ctrl(): return None

        if not isinstance(left, int | float | bool) or not isinstance(right, int | float | bool):
            ASTNode.add_ctrl(Token.ERROR, [
                Token.VALUEERROR, self.getline(),
                f'{ASTNode.format_data(left, src=True)} {Token.token(Token.DIVIDE)} '
                f'{ASTNode.format_data(right, src=True)} são incompatíveis'
            ])
            return None

        return left ** right