# ==========================================
# PARSER.PY - Gerador de àrvores AST
# ==========================================
from afri.model.lexer import Lexer
from afri.model.node import *

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.token = self.lexer.next()

    def eat(self, token_type):
        if self.token.type == token_type:
            self.token = self.lexer.next()
        else:
            raise SyntaxError(f"Token inesperado: {self.token}. Esperado: {token_type}")

    def factor(self):
        token = self.token
        if token.type in (Token.INT, Token.FLOAT):
            self.eat(token.type)
            return NumberNode(token)

        elif token.type == Token.BOOLEAN:
            self.eat(Token.BOOLEAN)
            return BooleanNode(token)

        elif token.type == Token.STRING:
            self.eat(Token.STRING)
            return StringNode(token)

        elif token.type == Token.ID:
            self.eat(Token.ID)
            return VariableNode(token)

        raise SyntaxError(f"Sintaxe inválida no factor: {token}")

    def term(self):
        node = self.factor()
        while self.token.type in (Token.MULTIPLY, Token.DIViDE):
            op_token = self.token
            self.eat(self.token.type)
            node = BinOpNode(left=node, token=op_token, right=self.factor())
        return node

    def expr(self):
        node = self.term()
        while self.token.type in (Token.PLUS, Token.MINUS):
            op_token = self.token
            self.eat(self.token.type)
            node = BinOpNode(left=node, token=op_token, right=self.term())
        return node

    def statement(self):
        if self.token.type == Token.VER:
            self.eat(Token.VER)
            return VerNode(arg=self.expr())

        if self.token.type == Token.RECEBER:
            self.eat(Token.RECEBER)
            if self.token.type == Token.ID:
                var_node = VariableNode(self.token)
                self.eat(Token.ID)
                return ReceberNode(var=var_node)
            else:
                raise SyntaxError("Esperado nome de variável após 'receber'.")

        if self.token.type == Token.ID:
            var_node = VariableNode(self.token)
            self.eat(Token.ID)
            if self.token.type == Token.ASSIGN:
                self.eat(Token.ASSIGN)
                expr_node = self.expr()
                return AssignNode(left=var_node, right=expr_node)
            else:
                raise SyntaxError("Instrução inválida baseada em identificador.")

        return self.expr()

    def parse(self):
        nodes = []

        while self.token.value:
            nodes.append(self.statement())
        return nodes