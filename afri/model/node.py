# ==========================================
# NODE.PY - Árvores AST
# ==========================================
from .token import Token

class ASTNode:
    FEATURE = {
        # incluir características
        # 'value': str | list[str],
        # 'token': str,
        #  'type': str,
    }
    _NODES = {
        # include nodes
        # Token.INTEGER: NumberNode
    }
    _CONTROLS = {
        # control exec
        # key: value
    }

    def __init__(self, value: object):
        self._value = value
        self._line = (0, 0)

    @staticmethod
    def ctrl(exec_func):
        def ctrl_exec(*args, **kwargs):
            if not ASTNode.exs_ctrl():
                return exec_func(*args, **kwargs)
            return None

        return ctrl_exec

    def exec(self, **kwargs):
        return None

    @staticmethod
    def register(*args):
        for arg in args:
            if arg not in ASTNode._NODES:
                if Token.register(arg.FEATURE):
                    ASTNode._NODES[arg.FEATURE['token']] = arg

    @staticmethod
    def include_nodes(**kwargs):
        for key, value in kwargs.items():
            if key not in ASTNode._NODES:
                ASTNode._NODES[key] = value

    @staticmethod
    def add_ctrl(key, value):
        ASTNode._CONTROLS.update({key: value})

    @staticmethod
    def get_ctrl(key):
        if key in ASTNode._CONTROLS:
            return ASTNode._CONTROLS[key]
        return None

    @staticmethod
    def del_ctrl(key):
        ASTNode._CONTROLS.pop(key)

    @staticmethod
    def exs_ctrl():
        return len(ASTNode._CONTROLS)

    @staticmethod
    def all_ctrl():
        return { **ASTNode._CONTROLS }

    @staticmethod
    def get_node(token: Token, **kwargs):
        if token.type in ASTNode._NODES:
            node = ASTNode._NODES[token.type]
            value = token.value
            if 'value' in kwargs:
                value = kwargs['value']

            if issubclass(node, KeyNode):
                if isinstance(value, Block):
                    node = KeyBlockNode

            if issubclass(node, IsolateNode):
                if isinstance(value, Block):
                    node = IsolateBlockNode

            if issubclass(node, SeparateNode):
                if (isinstance(kwargs['left'], Block) or
                    isinstance(kwargs['right'], Block)):
                    node = SeparateBlockNode

            if issubclass(node, UniOpNode):
                return node(value, kwargs['right']).setline(token.line)

            if issubclass(node, BinOpNode):
                return node.order_fat(node, token, kwargs['left'], kwargs['right'])

            if issubclass(node, FunctionNode):
                return node(value, kwargs['args']).setline(token.line)
            return node(value).setline(token.line)
        return None

    @staticmethod
    def get_class_node(token: Token):
        if token.type in ASTNode._NODES:
            return ASTNode._NODES[token.type]
        return None

    @staticmethod
    def view(value):
        context = ASTNode.format_data(value).replace('\n', ' ').replace('\t', ' ')
        dots = '...' if len(context) > 29 else ''
        return context[:29] + dots

    @staticmethod
    def format_data(data, src=False):
        if data is None:
            return Token.token(Token.NULL)

        if isinstance(data, bool):
            return BooleanNode.format(data)

        if src and isinstance(data, str):
            return StringNode.format(data)

        if isinstance(data, list):
            content = '('
            for i in range(len(data)):
                if len(content) - 1: content += ', '
                if isinstance(data[i], str):
                    content += StringNode.format(data[i])
                else:
                    content += ASTNode.format_data(data[i])
            return content + ')'
        return str(data)

    @property
    def value(self):
        return self._value

    def setline(self, line: tuple[int, int]):
        if not self._line[0]:
            self._line = line
        return self

    def getline(self) -> tuple[int, int]:
        return self._line

    def __repr__(self):
        return f"{self._value}"

class BinOpNode(ASTNode):
    def __init__(self, value: object, left: ASTNode, right: ASTNode):
        super().__init__(value)
        self._left: ASTNode = left
        self._right: ASTNode = right

    @staticmethod
    def order_fat(node, token: Token, left: ASTNode, right: ASTNode):
        if isinstance(right, BinOpNode):
            right: BinOpNode = right
            if right.center and (
                node.FEATURE['order'] < right.FEATURE['order']
            ):
                return ASTNode.get_node(Token(
                    right.FEATURE['token'],
                    Token.token(right.FEATURE['token']),
                    right.getline()
                ), **{
                    'left': BinOpNode.order_fat(node, token, left, right.left),
                    'right': right.right
                })

        return node(token.value, left, right).setline(token.line)

    @property
    def left(self) -> ASTNode:
        return self._left

    @property
    def right(self) -> ASTNode:
        return self._right

    @property
    def center(self) -> bool:
        return False

    def __repr__(self):
        return f"{self._left} {self._value} {self._right}"

class UniOpNode(ASTNode):
    def __init__(self, value: object, right: ASTNode):
        super().__init__(value)
        self._right: ASTNode = right

    @property
    def right(self) -> ASTNode:
        return self._right

    def __repr__(self):
        return f"{self._value} {self._right}"

class FunctionNode(ASTNode):
    def __init__(self, value: object, args: ASTNode):
        super().__init__(value)
        self._args: ASTNode = args

    @ASTNode.ctrl
    def exec(self, **kwargs):
        from .nodes.group import SeparateNode

        if not isinstance(self.args, EOFNode):
            args = SeparateNode.to_list(self.args)
        else:
            args = []
        return self._main(*args, **kwargs)

    def _main(self, *args, **kwargs) -> object:
        pass

    @property
    def args(self) -> ASTNode:
        return self._args

    def __repr__(self):
        return f"{self._value} {self._args}"

from .nodes import *
