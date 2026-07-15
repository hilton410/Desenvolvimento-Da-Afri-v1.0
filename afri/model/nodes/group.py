# ==================================================
# GROUP.PY - Arvóres AST para agrupamento de dados
# ==================================================
from . import Token, ASTNode, UniOpNode
from . import BinOpNode, EOFNode

class Block:
    def __repr__(self, sx='\t', sy=''):
        return super().__repr__()

class SeparateNode(BinOpNode):
    FEATURE = {
        'token': Token.SEPARATE,
        'type': Token.OPERATOR,
        'order': 8,
        'fat': True
    }

    def __init__(self, value: object, left: ASTNode, right: ASTNode):
        super().__init__(value, left, right)
        self._left: ASTNode = left
        self._right: ASTNode = right

    @staticmethod
    def to_list(separate: ASTNode, first=True) -> list[ASTNode]:
        params = []
        if isinstance(separate, SeparateNode):
            params = (
                SeparateNode.to_list(separate.left, False) +
                SeparateNode.to_list(separate.right, first)
            )
        else:
            if not first or not isinstance(separate, EOFNode):
                params.append(separate)
        return params

    @ASTNode.ctrl
    def exec(self, **kwargs):
        args = SeparateNode.to_list(self)
        for index, arg in enumerate(args):
            args[index] = arg.exec(**kwargs)
        return args

    @property
    def center(self) -> bool:
        return True

    def __repr__(self):
        return f"{self._left}, {self._right}"

class IsolateNode(ASTNode):
    FEATURE = {
        'token': Token.ISOLATE,
        'type': Token.GROUP,
    }

    @ASTNode.ctrl
    def exec(self, **kwargs):
        return self.value.exec(**kwargs)

    def __repr__(self):
        return f"({self.value})"

class KeyNode(UniOpNode):
    FEATURE = {
        'token': Token.KEY,
        'type': Token.GROUP,
        'uni': True
    }

    @ASTNode.ctrl
    def exec(self, **kwargs):
        value = self.value.exec(**kwargs)
        key = self.right.exec(**kwargs)
        if ASTNode.exs_ctrl(): return None
        try:
            return value[key]
        except TypeError:
            ASTNode.add_ctrl(Token.ERROR, [
                Token.VALUEERROR, self.getline(),
                f'o valor {ASTNode.format_data(value, src=True)} não possui '
                f'uma chave [{ASTNode.format_data(key, src=True)}]'
            ])
            return None

    def __repr__(self):
        return f"{self.value}[{self.right}]"

class BlockNode(ASTNode, Block):
    FEATURE = {
        'token': Token.ALINE,
        'type': Token.GROUP,
        'fat': True
    }

    @ASTNode.ctrl
    def exec(self, **kwargs):
        for value in self.value:
            value.exec(**kwargs)
            if ASTNode.exs_ctrl():
                break

    def __repr__(self, sx='\t', sy=''):
        return (
            '{\n'
                f'{sx}{
                    f'\n{sx}'.join([(
                        str(value) if not isinstance(value, Block)
                        else value.__repr__(sx='\t' + sx, sy=sx)
                    ) for value in self.value])
                }\n{sy}'
            '}'
        )

class IsolateBlockNode(IsolateNode, Block):
    def __repr__(self, sx='\t', sy=''):
        if isinstance(self.value, Block):
            return self.value.__repr__(sx=sx, sy=sy)
        return super().__repr__()

class KeyBlockNode(KeyNode, Block):
    def __repr__(self, sx='\t', sy=''):
        if isinstance(self.value, Block):
            return self.value.__repr__(sx=sx, sy=sy)
        return super().__repr__()

class SeparateBlockNode(SeparateNode, Block):
    def __repr__(self, sx='\t', sy=''):
        return f"{
            self.left.__repr__(sx=sx, sy=sy) if isinstance(self.left, Block) else self.left.__repr__()
        }, {            
            self.right.__repr__(sx=sx, sy=sy) if isinstance(self.right, Block) else self.right.__repr__()
        }"