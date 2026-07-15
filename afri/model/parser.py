# ==========================================
# PARSER.PY - Gerador de àrvores AST
# ==========================================
from .lexer import Lexer
from .node import *

class Parser:
    def __init__(self, lexer: Lexer):
        self.groups = []
        self.errors = []
        self.scopes = []
        self.no_scopes = []

        self.lexer = lexer
        self.last_token = None
        self.token = self.lexer.next()

    def error(self, e: str, token: Token, name=Token.SYNTAXERROR):
        self.errors.append(f'{name}: {e}, linha {token.line}')

    def factor(self) -> ASTNode:
        if value_token := Token.is_group(self.token.type, index=0):
            size = len(self.groups)
            type_token = self.token.type
            self.token = self.lexer.next()
            self.groups.append(value_token.type)

            value = []
            right = ASTNode.get_node(Token(Token.EOF, ''))
            if Token.is_group(type_token, index=0, fat=True):
                while len(self.groups) != size:
                    node = self.statement()
                    if not isinstance(node, EOFNode):
                        value.append(node)
            else:
                value = self.expression()

            if isinstance(value, EOFNode):
                self.error(f"a expressão não pode estar vazia '{'...'.join(value_token.value)}'", value_token)

            if Token.is_group(type_token, index=0, uni=True):
                value, right = right, value
                if isinstance(value, EOFNode):
                    self.error(f"era esperado uma expressão conectada à '{'...'.join(value_token.value)}'", value_token)

            node = ASTNode.get_node(value_token, **{
                'value': value,
                'right': right
            })
            if len(self.groups) != size:
               self.error(f"a expressão foi aberta mas não fechada '{'...'.join(value_token.value)}'", value_token)
            return node

        value_token = self.token
        if Token.is_function(self.token.type):
            self.token = self.lexer.next()
            return ASTNode.get_node(value_token, **{
                'args': self.expression(),
            })

        if self.token.type == Token.FAT_STRING:
            self.token = self.lexer.next()
            self.error(f"o texto não foi fechado '{ASTNode.view(self.token.value)}'", value_token)
            return ASTNode.get_node(Token(Token.STRING, value_token.value, value_token.line))

        if Token.is_value(self.token.type):
            self.token = self.lexer.next()
            return ASTNode.get_node(value_token)

        if Token.is_operator(self.token.type, order=0, uni=True):
            self.token = self.lexer.next()
            value = self.expression(fat=False)
            if isinstance(value, EOFNode):
                self.error(f"era esperado uma expressão depois de '{value_token.value}'", value_token)
            return ASTNode.get_node(value_token, **{
                'right': value
            })

        if self.token.type != Token.EOF:
            self.error(f"a expressão '{value_token.value}' não correspondeu as espectativas", value_token)
            value_token = Token(Token.EOF, '')

        elif len(self.token.value):
            self.error(f"caracter inválido '{value_token.value}'", value_token)
        self.token = self.lexer.next()

        return ASTNode.get_node(value_token)

    def expression(self, order=1, maxy=Token.operator_order_max(), node=None, fat=True):
        if self.token.type == Token.END:
            if order == 1:
                self.token = self.lexer.next()
            return node or ASTNode.get_node(Token(Token.EOF, ''))

        if value_token := Token.is_group(self.token.type, index=1):
            if len(self.groups) > 0 and self.groups[-1] == value_token.type:
                if order == 1:
                    self.groups.pop()
                    self.last_token = self.token
                    self.token = self.lexer.next()
                return node or ASTNode.get_node(Token(Token.EOF, ''))
            else:
                self.error(f"não pode fechar se nunca se abriu '{'...'.join(value_token.value)}'", value_token)

        repeat = order < Token.operator_order_max()
        if node is None:
            node = self.expression(order + 1, maxy) if repeat else self.factor()

        if self.token.type == Token.END:
            if order == 1:
                self.token = self.lexer.next()
            return node

        if self.last_token and Token.is_group(self.last_token.type, index=1):
            if 'type' in node.FEATURE and node.FEATURE['type'] == Token.GROUP:
                 self.last_token = None
            else:
                return node

        if value_token := Token.is_group(self.token.type, index=0, uni=True):
            size = len(self.groups)
            self.token = self.lexer.next()
            self.groups.append(value_token.type)

            node = ASTNode.get_node(value_token, **{
                'value': node,
                'right': self.expression()
            })

            if len(self.groups) != size:
               self.error(f"a expressão foi aberta mas não fechada '{'...'.join(value_token.value)}'", value_token)

        while fat and Token.is_operator(self.token.type, order=order) and order < maxy:
            if value_token := Token.is_group(self.token.type, index=1):
                if len(self.groups) > 0 and self.groups[-1] == value_token.type:
                    if order == 1:
                        self.groups.pop()
                        self.last_token = self.token
                        self.token = self.lexer.next()
                else:
                    self.error(f"a expressão foi aberta mas não fechada '{'...'.join(value_token.value)}'", self.token)
                    self.token = self.lexer.next()
                break


            op_token = self.token
            self.token = self.lexer.next()

            if Token.is_operator(op_token.type, order=order, fat=True):
                node = ASTNode.get_node(op_token, **{
                    'left': node,
                    'right': self.expression(1, order) if repeat else self.factor()
                })

                if self.last_token and Token.is_group(self.last_token.type, index=1):
                    return node
                elif order + 1 < maxy:
                    for i in range(order + 1, maxy):
                        nodex = self.expression(i, maxy, node)
                        if nodex != node:
                            node = nodex
                            break
            else:
                node = ASTNode.get_node(op_token, **{
                    'left': node,
                    'right': self.expression(order + 1, maxy) if repeat else self.factor()
                })

            if isinstance(node.right, EOFNode) and not isinstance(node, SeparateNode):
                self.error(f"o operador '{op_token.value}' ainda precisa de um membro direito "
                                  f"antes de finalizar a expressão", op_token)
        return node

    def template(self, template: dict, template_args: list, token_value):
        express = None
        token = self.token
        if 'isistance' in template:
            if not express:
                express = self.statement()
            for instance in template['isistance']:
                if isinstance(express, instance):
                    if issubclass(instance, BlockNode) and 'body' in template:
                        for line in express.value:
                            for class_ast in template['body']:
                                if isinstance(line, class_ast):
                                    break
                            else:
                                self.error(
                                    f"foi encotrado a expressão '{ASTNode.view(line)}' que não deveria "
                                    f"fazer parte do escopo de '{token_value}'", token
                                )
                    break
            else:
                if 'optional' not in template or not template['optional']:
                    self.error(f"a estrutura de '{token_value}' está {
                        "incompleta" if isinstance(express, EOFNode) else
                        f"recebendo '{ASTNode.view(express)}' uma expressão inválida "
                        f"para a posição actual"
                    }", token)
                express = ASTNode.get_node(Token(Token.EOF, ''))

        if 'no_isistance' in template:
            if not express:
                express = self.statement()
            for instance in template['no_isistance']:
                if not isinstance(express, instance):
                    break
            else:
                if 'optional' not in template or not template['optional']:
                    self.error(f"a estrutura de '{token_value}' está {
                        "incompleta" if isinstance(express, EOFNode) else
                        f"recebendo '{ASTNode.view(express)}' uma expressão inválida "
                        f"para a posição actual"
                    }", token)
                express = ASTNode.get_node(Token(Token.EOF, ''))

        if 'token' in template:
            if self.token.type == template['token']:
                self.token = self.lexer.next()
                if 'template' in template:
                    for template2 in template['template']:
                        self.template(template2, template_args, token_value)
            else:
                if 'optional' not in template or not template['optional']:
                    self.error(f"a estrutura de '{token_value}' está {
                        "incompleta" if isinstance(express, EOFNode) else
                        f"recebendo '{ASTNode.view(express)}' uma expressão inválida "
                        f"para a posição actual"
                    }", token)
                template_args.append(ASTNode.get_node(Token(Token.EOF, '')))

        if express:
            template_args.append(express)

    def statement(self):
        if Token.is_block(self.token.type):
            node = ASTNode.get_class_node(self.token)
            token = self.token
            self.token = self.lexer.next()
            self.scopes.append(node)

            template_args = []
            token_value = Token.token(node.FEATURE['token'])
            for template in node.FEATURE['template']:
                self.template(template, template_args, token_value)
            self.scopes.pop()

            if 'scope' in node.FEATURE and len(self.scopes):
                for scope in node.FEATURE['scope']:
                    if scope in self.scopes:
                        break
                else:
                    self.error(f"a estrutura de '{token_value}' está no escopo {
                        f"de '{Token.token(self.scopes[-1].FEATURE['token'])}'"
                        if len(self.scopes) else "principal"
                    } que é inválido", token)

            if 'init_scope' in node.FEATURE and len(self.scopes):
                for scope in node.FEATURE['init_scope']:
                    if scope == self.scopes[-1]:
                        break
                else:
                    self.error(f"a estrutura de '{token_value}' está no escopo {
                        f"de '{Token.token(self.scopes[-1].FEATURE['token'])}'"
                        if len(self.scopes) else "principal"
                    } que é inválido", token)
            return node(template_args).setline(token.line)
        else:
            return self.expression()

    def parse(self):
        nodes = []
        # print("----------------------------------------------")
        while self.token.value != '':
            node = self.statement()
            # print(node)
            if not isinstance(node, EOFNode):
                nodes.append(node)
        # print("----------------------------------------------")
        return nodes
