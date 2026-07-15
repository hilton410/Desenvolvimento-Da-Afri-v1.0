# ==================================================
# AFRIINTERPRETER.PY - Interpretador de código
# ==================================================
from .model.parser import *

class AfriInterpreter:
    def __init__(self):
        self._kwargs = {
            'get_variable': self._get_variable,
            'set_variable': self._set_variable
        }
        self._table_variables = {}

    def run(self, code: str):
        lexer = Lexer(code)
        parser = Parser(lexer)

        value = None
        nodes = parser.parse()

        if not len(parser.errors):
            for node in nodes:
                value = node.exec(**self._kwargs)
                if ASTNode.exs_ctrl():
                    break

        output = ASTNode.all_ctrl()
        for key in output.keys():
            ASTNode.del_ctrl(key)
        output.update({
            'result': value,
            'parser_errors': parser.errors,
            'afri': ASTNode.format_data(value, src=True),
        })
        return output

    def _get_variable(self, name: str, node: ASTNode, error=False):
        if name in self._table_variables:
            return self._table_variables[name]

        if error:
            ASTNode.add_ctrl(Token.ERROR, [
                Token.VALUEERROR, node.getline(),
                f"a variável '{name}' não existe"
            ])
        return None

    def _set_variable(self, name: str, value: object, node: ASTNode, error=False):
        self._get_variable(name, node, error)
        self._table_variables[name] = value