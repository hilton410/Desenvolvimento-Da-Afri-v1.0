# ==================================================
# TYPE.PY - Arvóres AST para tipos de dados
# ==================================================
from . import ASTNode

class NumberNode(ASTNode):
    @ASTNode.ctrl
    def exec(self, **kwargs):
        return self.value

class StringNode(ASTNode):
    @ASTNode.ctrl
    def exec(self, **kwargs):
        return self.value

    @staticmethod
    def format(data):
        return f'"{str(data).replace('"', '\\"')}"'

    def __repr__(self):
        return self.format(self.value)

class BooleanNode(ASTNode):
    @staticmethod
    def format(data):
        return "verdade" if data else "falso"

    @ASTNode.ctrl
    def exec(self, **kwargs):
        return self.value == "verdade"

class VariableNode(ASTNode):
    @ASTNode.ctrl
    def exec(self, **kwargs):
        return kwargs['get_variable'](self.value, self, True)

class NullNode(ASTNode):
    @ASTNode.ctrl
    def exec(self, **kwargs):
        return None

class EOFNode(ASTNode):
    @ASTNode.ctrl
    def exec(self, **kwargs):
        return None

    def __repr__(self):
        return ''