# ==============================================================
# OPERATOR_ASSIGN.PY - Arvóres AST para operadores de atribuição
# ==============================================================
from . import Token, ASTNode, BinOpNode, VariableNode, KeyNode
from . import PlusNode, MinusNode, MultiplyNode
from . import DivideNode, ModuleNode, PowNode

class Assign:
    FEATURE = {
        'type': Token.OPERATOR,
        'order': 7,
        'fat': True
    }

class AssignNode(BinOpNode, Assign):
    FEATURE = {
        'token': Token.ASSIGN,
        **Assign.FEATURE
    }

    @ASTNode.ctrl
    def exec(self, **kwargs):
        if isinstance(self.left, VariableNode):
            value = self.right.exec(**kwargs)
            if ASTNode.exs_ctrl(): return None

            kwargs['set_variable'](self.left.value, value, self)
            return kwargs['get_variable'](self.left.value, self)

        elif isinstance(self.left, KeyNode):
            array = self.left.value.exec(**kwargs)
            index = self.left.right.exec(**kwargs)

            value = self.right.exec(**kwargs)
            if ASTNode.exs_ctrl(): return None

            array[index] = value
            return array[index]
        else:
            ASTNode.add_ctrl(Token.ERROR, [
                Token.VALUEERROR, self.getline(),
                f"esperado nome de variável antes do operador '{Token.token(Token.ASSIGN)}'"
            ])
            return None

    @property
    def center(self):
        return True

class PlusAssignNode(PlusNode, Assign):
    FEATURE = {
        'value': Token.token(Token.PLUS) + Token.token(Token.ASSIGN),
        'token': Token.ASSIGN + f'_{Token.PLUS}',
        **Assign.FEATURE
    }

    @ASTNode.ctrl
    def exec(self, **kwargs):
        if isinstance(self.left, VariableNode):
            value = super().exec(**kwargs)
            if ASTNode.exs_ctrl(): return None

            kwargs['set_variable'](self.left.value, value, self, error=True)
            return kwargs['get_variable'](self.left.value, self)

        elif isinstance(self.left, KeyNode):
            array = self.left.value.exec(**kwargs)
            index = self.left.right.exec(**kwargs)

            value = super().exec(**kwargs)
            if ASTNode.exs_ctrl(): return None

            array[index] = value
            return array[index]
        else:
            ASTNode.add_ctrl(Token.ERROR, [
                Token.VALUEERROR, self.getline(),
                f"esperado nome de variável antes do operador '{Token.token(self.FEATURE['token'])}'"
            ])
            return None

    @property
    def center(self):
        return True

class MinusAssignNode(MinusNode, Assign):
    FEATURE = {
        'value': Token.token(Token.MINUS) + Token.token(Token.ASSIGN),
        'token': Token.ASSIGN + f'_{Token.MINUS}',
        **Assign.FEATURE
    }

    @ASTNode.ctrl
    def exec(self, **kwargs):
        if isinstance(self.left, VariableNode):
            value = super().exec(**kwargs)
            if ASTNode.exs_ctrl(): return None

            kwargs['set_variable'](self.left.value, value, self, error=True)
            return kwargs['get_variable'](self.left.value, self)

        elif isinstance(self.left, KeyNode):
            array = self.left.value.exec(**kwargs)
            index = self.left.right.exec(**kwargs)

            value = super().exec(**kwargs)
            if ASTNode.exs_ctrl(): return None

            array[index] = value
            return array[index]
        else:
            ASTNode.add_ctrl(Token.ERROR, [
                Token.VALUEERROR, self.getline(),
                f"esperado nome de variável antes do operador '{Token.token(self.FEATURE['token'])}'"
            ])
            return None

    @property
    def center(self):
        return True

class MultiplyAssignNode(MultiplyNode, Assign):
    FEATURE = {
        'value': Token.token(Token.MULTIPLY) + Token.token(Token.ASSIGN),
        'token': Token.ASSIGN + f'_{Token.MULTIPLY}',
        **Assign.FEATURE
    }

    @ASTNode.ctrl
    def exec(self, **kwargs):
        if isinstance(self.left, VariableNode):
            value = super().exec(**kwargs)
            if ASTNode.exs_ctrl(): return None

            kwargs['set_variable'](self.left.value, value, self, error=True)
            return kwargs['get_variable'](self.left.value, self)

        elif isinstance(self.left, KeyNode):
            array = self.left.value.exec(**kwargs)
            index = self.left.right.exec(**kwargs)

            value = super().exec(**kwargs)
            if ASTNode.exs_ctrl(): return None

            array[index] = value
            return array[index]
        else:
            ASTNode.add_ctrl(Token.ERROR, [
                Token.VALUEERROR, self.getline(),
                f"esperado nome de variável antes do operador '{Token.token(self.FEATURE['token'])}'"
            ])
            return None

    @property
    def center(self):
        return True

class DivideAssignNode(DivideNode, Assign):
    FEATURE = {
        'value': Token.token(Token.DIVIDE) + Token.token(Token.ASSIGN),
        'token': Token.ASSIGN + f'_{Token.DIVIDE}',
        **Assign.FEATURE
    }

    @ASTNode.ctrl
    def exec(self, **kwargs):
        if isinstance(self.left, VariableNode):
            value = super().exec(**kwargs)
            if ASTNode.exs_ctrl(): return None

            kwargs['set_variable'](self.left.value, value, self, error=True)
            return kwargs['get_variable'](self.left.value, self)

        elif isinstance(self.left, KeyNode):
            array = self.left.value.exec(**kwargs)
            index = self.left.right.exec(**kwargs)

            value = super().exec(**kwargs)
            if ASTNode.exs_ctrl(): return None

            array[index] = value
            return array[index]
        else:
            ASTNode.add_ctrl(Token.ERROR, [
                Token.VALUEERROR, self.getline(),
                f"esperado nome de variável antes do operador '{Token.token(self.FEATURE['token'])}'"
            ])
            return None

    @property
    def center(self):
        return True

class ModuleAssignNode(ModuleNode, Assign):
    FEATURE = {
        'value': Token.token(Token.MODULE) + Token.token(Token.ASSIGN),
        'token': Token.ASSIGN + f'_{Token.MODULE}',
        **Assign.FEATURE
    }

    @ASTNode.ctrl
    def exec(self, **kwargs):
        if isinstance(self.left, VariableNode):
            value = super().exec(**kwargs)
            if ASTNode.exs_ctrl(): return None

            kwargs['set_variable'](self.left.value, value, self, error=True)
            return kwargs['get_variable'](self.left.value, self)

        elif isinstance(self.left, KeyNode):
            array = self.left.value.exec(**kwargs)
            index = self.left.right.exec(**kwargs)

            value = super().exec(**kwargs)
            if ASTNode.exs_ctrl(): return None

            array[index] = value
            return array[index]
        else:
            ASTNode.add_ctrl(Token.ERROR, [
                Token.VALUEERROR, self.getline(),
                f"esperado nome de variável antes do operador '{Token.token(self.FEATURE['token'])}'"
            ])
            return None

    @property
    def center(self):
        return True

class PowAssignNode(PowNode, Assign):
    FEATURE = {
        'value': Token.token(Token.POW) + Token.token(Token.ASSIGN),
        'token': Token.ASSIGN + f'_{Token.POW}',
        **Assign.FEATURE
    }

    @ASTNode.ctrl
    def exec(self, **kwargs):
        if isinstance(self.left, VariableNode):
            value = super().exec(**kwargs)
            if ASTNode.exs_ctrl(): return None

            kwargs['set_variable'](self.left.value, value, self, error=True)
            return kwargs['get_variable'](self.left.value, self)

        elif isinstance(self.left, KeyNode):
            array = self.left.value.exec(**kwargs)
            index = self.left.right.exec(**kwargs)

            value = super().exec(**kwargs)
            if ASTNode.exs_ctrl(): return None

            array[index] = value
            return array[index]
        else:
            ASTNode.add_ctrl(Token.ERROR, [
                Token.VALUEERROR, self.getline(),
                f"esperado nome de variável antes do operador '{Token.token(self.FEATURE['token'])}'"
            ])
            return None

    @property
    def center(self):
        return True