from afri.model.parser import *

class AfriInterpreter:
    def __init__(self):
        self._table_variables = {}

    def run(self, code: str):
        lexer = Lexer(code)
        parser = Parser(lexer)

        for node in parser.parse():
            self.exec(node)

    def exec(self, node: ASTNode):
        if isinstance(node, NumberNode):
            return node.value

        if isinstance(node, BooleanNode):
            return node.value

        if isinstance(node, StringNode):
            return str(node.value)

        if isinstance(node, VariableNode):
            nome_var = node.value
            if nome_var in self._table_variables:
                return self._table_variables[nome_var]
            raise Exception(f"Erro de Execução: A variável '{nome_var}' não existe.")

        if isinstance(node, AssignNode):
            nome_var = node.left.value
            valor = self.exec(node.right)
            self._table_variables[nome_var] = valor
            return valor

        if isinstance(node, BinOpNode):
            esquerda = self.exec(node.left)
            direita = self.exec(node.right)
            tipo_op = node.token.type

            if tipo_op == Token.PLUS:
                if isinstance(esquerda, str) or isinstance(direita, str):
                    return str(esquerda) + str(direita)
                return esquerda + direita

            elif tipo_op == Token.MINUS:
                return esquerda - direita

            elif tipo_op == Token.MULTIPLY:
                return esquerda * direita

            elif tipo_op == Token.DIViDE:
                if direita == 0:
                    raise ZeroDivisionError("Erro: Divisão por zero não permitida no afri.")
                return esquerda / direita

        if isinstance(node, VerNode):
            resultado = self.exec(node.arg)
            print(resultado)
            return resultado

        if isinstance(node, ReceberNode):
            nome_var = node.var.value
            valor_digitado = input().strip()

            # Mapeamento dinâmico inteligente no input do afri
            if valor_digitado == "verdade":
                self._table_variables[nome_var] = True
            elif valor_digitado == "falso":
                self._table_variables[nome_var] = False
            elif valor_digitado.isdigit():
                self._table_variables[nome_var] = int(valor_digitado)
            else:
                try:
                    self._table_variables[nome_var] = float(valor_digitado)
                except ValueError:
                    self._table_variables[nome_var] = valor_digitado

            return self._table_variables[nome_var]

        raise Exception(f"Erro de Execução: Tipo de nó desconhecido: {type(node)}")