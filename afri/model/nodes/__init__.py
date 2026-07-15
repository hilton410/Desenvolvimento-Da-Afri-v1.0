from ..token import Token
from ..node import ASTNode
from ..node import BinOpNode
from ..node import UniOpNode, FunctionNode

# procedimento de importação
from .type import *
from .group import *
from .operator import *
from .operator_logic import *
from .operator_assign import *
from .function import *
from .block import *

# inclução de tipo de dados
ASTNode.include_nodes(**{
    Token.INTEGER: NumberNode,
    Token.FLOAT: NumberNode,
    Token.BOOLEAN: BooleanNode,
    Token.STRING: StringNode,
    Token.NULL: NullNode,
    Token.ID: VariableNode,
    Token.EOF: EOFNode,
})

# registro de operadores
ASTNode.register(
    PlusNode, MinusNode,
    MultiplyNode, DivideNode,
    ModuleNode, PowNode,

    LessNode, GreatNode,
    LessEqualNone, GreatEqualNone,
    EqualNode, NoEqualNode,
    AndNode, OrNode, NotNode,

    AssignNode, PlusAssignNode,
    MinusAssignNode, MultiplyAssignNode,
    DivideAssignNode, ModuleAssignNode,
    PowAssignNode
)

# registro de grupos
ASTNode.register(
    IsolateNode, SeparateNode,
    BlockNode, KeyNode,
    IsolateBlockNode, SeparateBlockNode,
)

# registro de blocos
ASTNode.register(
    IfNode, SwitchNode,
    CaseNode, DefaultNode,

    WhileNode, DoWhileNode,
    ForNode, BreakNode, ContinueNode,
)

# registro de funções
ASTNode.register(
    DefVerNode, DefReceberNode,
)