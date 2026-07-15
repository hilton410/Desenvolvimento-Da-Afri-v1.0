# ==================================================
# BLOCK.PY - Arvóres AST para estruturas de controle
# ==================================================
from . import Token, ASTNode, BlockNode, Block
from . import Assign, SeparateNode, EOFNode

class IfNode(ASTNode, Block):
    FEATURE = {
        'token': Token.IF,
        'type': Token.BLOCK,
        'template': [
            { 'isistance': [ASTNode], 'no_isistance': [Block] },
            { 'isistance': [ASTNode] },
            { 'optional': True, 'token': Token.ELSE, 'template': [{ 'isistance': [ASTNode] }] },
        ]
    }

    @ASTNode.ctrl
    def exec(self, **kwargs):
        if isinstance(self.value, str):
            return

        if self.value[0].exec(**kwargs):
            self.value[1].exec(**kwargs)
        elif len(self.value) >= 2:
            self.value[2].exec(**kwargs)

    def __repr__(self, sx='\t', sy=''):
        if isinstance(self.value, str):
            return self.value

        sz = ' ' if isinstance(self.value[1], BlockNode) else f'\n' + sx
        return (
            f'{Token.token(Token.IF)} {self.value[0]}{sz}'
            f'{self.value[1].__repr__(sx='\t' + sy, sy=sy)
                if isinstance(self.value[1], Block) else self.value[1]
            }'
            f'{
                f'' if isinstance(self.value[2], EOFNode) else '\n'
                f'{sy + Token.token(Token.ELSE)} {self.value[2].__repr__(sx='\t' + sy, sy=sy)
                    if isinstance(self.value[2], Block) else self.value[2]
                }'
            }'
        )

class WhileNode(ASTNode, Block):
    FEATURE = {
        'token': Token.WHILE,
        'type': Token.BLOCK,
        'template': [
            { 'isistance': [ASTNode], 'no_isistance': [Block] },
            { 'isistance': [ASTNode] },
        ],
    }

    @ASTNode.ctrl
    def exec(self, **kwargs):
        if isinstance(self.value, str):
            return

        while self.value[0].exec(**kwargs):
            self.value[1].exec(**kwargs)
            if ASTNode.get_ctrl(Token.BREAK):
                ASTNode.del_ctrl(Token.BREAK)
                break

            if ASTNode.get_ctrl(Token.CONTINUE):
                ASTNode.del_ctrl(Token.CONTINUE)

            if ASTNode.exs_ctrl():
                break

    def __repr__(self, sx='\t', sy=''):
        if isinstance(self.value, str):
            return self.value

        sz = ' ' if isinstance(self.value[1], BlockNode) else f'\n' + sx
        return (
            f'{Token.token(Token.WHILE)} {self.value[0]}{sz}'
            f'{self.value[1].__repr__(sx='\t' + sy, sy=sy) if isinstance(self.value[1], Block) else self.value[1]}'
        )

class DoWhileNode(ASTNode, Block):
    FEATURE = {
        'token': Token.DO,
        'type': Token.BLOCK,
        'template': [
            { 'isistance': [ASTNode] },
            { 'token': Token.WHILE, 'template': [{ 'isistance': [ASTNode], 'no_isistance': [Block] }] },
        ],
    }

    @ASTNode.ctrl
    def exec(self, **kwargs):
        if isinstance(self.value, str):
            return

        self.value[0].exec(**kwargs)
        if ASTNode.get_ctrl(Token.BREAK):
            ASTNode.del_ctrl(Token.BREAK)
            return

        if ASTNode.get_ctrl(Token.CONTINUE):
            ASTNode.del_ctrl(Token.CONTINUE)

        if ASTNode.exs_ctrl():
            return

        while self.value[1].exec(**kwargs):
            self.value[0].exec(**kwargs)
            if ASTNode.get_ctrl(Token.ERROR):
                break

            if ASTNode.get_ctrl(Token.BREAK):
                ASTNode.del_ctrl(Token.BREAK)
                break

            if ASTNode.get_ctrl(Token.CONTINUE):
                ASTNode.del_ctrl(Token.CONTINUE)

            if ASTNode.exs_ctrl():
                break

    def __repr__(self, sx='\t', sy=''):
        if isinstance(self.value, str):
            return self.value

        sz = ' ' if isinstance(self.value[0], Block) else f'\n' + sx
        return (
            f'{Token.token(Token.DO)}{sz}'
            f'{self.value[0].__repr__(sx='\t' + sy, sy=sy) if isinstance(self.value[0], Block) else self.value[0]}\n'
            f'{Token.token(Token.WHILE)} {self.value[1]}'
        )

class ForNode(ASTNode, Block):
    FEATURE = {
        'token': Token.FOR,
        'type': Token.BLOCK,
        'template': [
            { 'optional': True, 'isistance': [Assign, SeparateNode], 'no_isistance': [Block] },
            { 'isistance': [ASTNode], 'no_isistance': [Block] },
            { 'optional': True, 'isistance': [Assign, SeparateNode], 'no_isistance': [Block] },
            { 'isistance': [ASTNode] },
        ],
    }
    @ASTNode.ctrl
    def exec(self, **kwargs):
        if isinstance(self.value, str):
            return

        if isinstance(self.value[0], SeparateNode):
            for index, node in enumerate(SeparateNode.to_list(self.value[0])):
                if not isinstance(node, Assign):
                    ASTNode.add_ctrl(Token.ERROR, [
                        Token.VALUEERROR, self.getline(),
                        f"No primeiro campo o elemento número '{index}' não é uma variável '{Token.token(Token.FOR)}'"
                    ])
                    return None

        elif not isinstance(self.value[0], Assign):
            ASTNode.add_ctrl(Token.ERROR, [
                Token.VALUEERROR, self.getline(),
                f"Deves passar apenas variáveis no primeiro campo de '{Token.token(Token.FOR)}'"
            ])
            return None

        self.value[0].exec(**kwargs)
        while self.value[1].exec(**kwargs):
            self.value[3].exec(**kwargs)
            if ASTNode.get_ctrl(Token.ERROR):
                break

            if ASTNode.get_ctrl(Token.BREAK):
                ASTNode.del_ctrl(Token.BREAK)
                break

            if ASTNode.get_ctrl(Token.CONTINUE):
                ASTNode.del_ctrl(Token.CONTINUE)

            if ASTNode.exs_ctrl():
                break
            self.value[2].exec(**kwargs)
        return None

    def __repr__(self, sx='\t', sy=''):
        if isinstance(self.value, str):
            return self.value

        sz = ' ' if isinstance(self.value[3], BlockNode) else f'\n' + sx
        return (
            f'{Token.token(Token.FOR)} {self.value[0]}; {self.value[1]}; {self.value[2]};{sz}'
            f'{self.value[3].__repr__(sx='\t' + sy, sy=sy) if isinstance(self.value[3], Block) else self.value[3]}'
        )

class CaseNode(ASTNode, Block):
    FEATURE = {
        'token': Token.CASE,
        'type': Token.BLOCK,
        'template': [
            { 'isistance': [ASTNode], 'no_isistance': [Block] },
            { 'isistance': [ASTNode] },
        ],
        'init_scope': [],
    }

    @ASTNode.ctrl
    def exec(self, **kwargs):
        self.value[1].exec(**kwargs)

    def __repr__(self, sx='\t', sy=''):
        if isinstance(self.value, str):
            return self.value

        sz = ' ' if isinstance(self.value[1], BlockNode) else f'\n' + sx
        return (
            f'{Token.token(Token.CASE)} {self.value[0]}{sz}'
            f'{self.value[1].__repr__(sx='\t' + sy, sy=sy) if isinstance(self.value[1], Block) else self.value[1]}'
        )

class DefaultNode(ASTNode, Block):
    FEATURE = {
        'token': Token.DEFAULT,
        'type': Token.BLOCK,
        'template': [
            { 'isistance': [ASTNode] },
        ],
        'init_scope': [],
    }

    @ASTNode.ctrl
    def exec(self, **kwargs):
        self.value[0].exec(**kwargs)

    def __repr__(self, sx='\t', sy=''):
        if isinstance(self.value, str):
            return self.value

        sz = ' ' if isinstance(self.value[0], BlockNode) else f'\n' + sx
        return (
            f'{Token.token(Token.DEFAULT)}{sz}'
            f'{self.value[0].__repr__(sx='\t' + sy, sy=sy) if isinstance(self.value[0], Block) else self.value[0]}'
        )

class SwitchNode(ASTNode, Block):
    FEATURE = {
        'token': Token.SWITCH,
        'type': Token.BLOCK,
        'template': [
            {'isistance': [ASTNode], 'no_isistance': [Block] },
            {'isistance': [BlockNode], 'body': [CaseNode, DefaultNode]}
        ],
    }

    @ASTNode.ctrl
    def exec(self, **kwargs):
        case_s = None
        default = None
        value = self.value[0].exec(**kwargs)
        for _case in self.value[1].value:
            if isinstance(_case, DefaultNode):
                default = _case
            elif case_s or _case.value[0].exec(**kwargs) == value:
                case_s = _case
                _case.exec(**kwargs)
                if ASTNode.get_ctrl(Token.BREAK):
                    ASTNode.del_ctrl(Token.BREAK)
                    return

                if ASTNode.exs_ctrl():
                    return
        if default:
            default.exec(**kwargs)

    def __repr__(self, sx='\t', sy=''):
        if isinstance(self.value, str):
            return self.value

        return (
            f'{Token.token(Token.SWITCH)} {self.value[0]} '
            f'{self.value[1].__repr__(sx='\t' + sy, sy=sy)}'
        )

class BreakNode(ASTNode, Block):
    FEATURE = {
        'token': Token.BREAK,
        'type': Token.BLOCK,
        'template': [],
        'scope': [],
    }

    @ASTNode.ctrl
    def exec(self, **kwargs):
        ASTNode.add_ctrl(Token.BREAK, True)

    def __repr__(self, sx='\t', sy=''):
        return Token.token(Token.BREAK)

class ContinueNode(ASTNode, Block):
    FEATURE = {
        'token': Token.CONTINUE,
        'type': Token.BLOCK,
        'template': [],
        'scope': [],
    }

    @ASTNode.ctrl
    def exec(self, **kwargs):
        ASTNode.add_ctrl(Token.CONTINUE, True)

    def __repr__(self, sx='\t', sy=''):
        return Token.token(Token.CONTINUE)

CaseNode.FEATURE['init_scope'] = [SwitchNode]
DefaultNode.FEATURE['init_scope'] = [SwitchNode]
BreakNode.FEATURE['scope'] = [WhileNode, ForNode, SwitchNode]
ContinueNode.FEATURE['scope'] = [WhileNode, ForNode, SwitchNode]