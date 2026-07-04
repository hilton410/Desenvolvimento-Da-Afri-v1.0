from afri.model.parser import *

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

        for node in parser.parse():
            node.exec(**self._kwargs)

    def _get_variable(self, name: str, error=False):
        if name in self._table_variables:
            return self._table_variables[name]

        if error:
            raise Exception(f"Erro de Execução: A variável '{name}' não existe.")
        return None

    def _set_variable(self, name: str, value: object, error=False):
        self._get_variable(name, error)
        self._table_variables[name] = value