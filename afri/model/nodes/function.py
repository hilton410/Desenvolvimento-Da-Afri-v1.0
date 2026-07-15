# ==================================================
# FUNCTION.PY - Arvóres AST para funções
# ==================================================
from . import Token, VariableNode, FunctionNode
from ..node import ASTNode

class DefVerNode(FunctionNode):
    FEATURE = {
        'value': 'ver',
        'type': Token.FUNCTION,
    }

    def _main(self, *args, **kwargs) -> object:
        args = list(args)
        for index, arg in enumerate(args):
            args[index] = ASTNode.format_data(arg.exec(**kwargs))
        if ASTNode.exs_ctrl(): return None

        print(', '.join(args))
        return None


class DefReceberNode(FunctionNode):
    FEATURE = {
        'value': 'receber',
        'type': Token.FUNCTION,
    }

    def _main(self, *args, **kwargs) -> object:
        if len(args) == 0:
            return None

        if not isinstance(args[0], VariableNode):
            ASTNode.add_ctrl(Token.ERROR, [
                Token.VALUEERROR.getline(),
                f"O argumento passado '{ASTNode.view(args[0])}' não é uma variável"
            ])

        name = args[0].value
        value = input().strip()
        if value == 'verdade':
            kwargs['set_variable'](name, True, self)

        elif value == 'falso':
            kwargs['set_variable'](name, False, self)

        elif value.isdigit():
            kwargs['set_variable'](name, int(value), self)
        else:
            try:
                kwargs['set_variable'](name, float(value), self)
            except ValueError:
                kwargs['set_variable'](name, value, self)

        return kwargs['get_variable'](name, True)