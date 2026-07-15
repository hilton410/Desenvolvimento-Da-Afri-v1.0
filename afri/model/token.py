# ==========================================
# TOKEN.PY - Tokens ou palavras chaves
# ==========================================

class Token:
    # Características
    BLOCK = 'BLOCO'
    GROUP = 'GROUPO'
    FUNCTION = 'FUNCAO'
    OPERATOR = 'OPERADOR'
    _OPERATOR_ORDER_MAX = 9
    _CHAR_MAX = 3

    # Tipos de dados
    INTEGER = 'INTEIRO'
    FLOAT = 'DECIMAL'
    BOOLEAN = 'BINARIO'
    STRING = 'TEXTO'
    FAT_STRING = 'TEXTO_SEM_FIM'
    NULL = 'NADA'

    # Identificadores
    ID = 'ID'
    EOF = 'EOF'
    END = 'FIM'

    # Controle de fluxo
    IF = 'SE'
    ELSE = 'SENAO'
    WHILE = 'ENQUANTO'
    DO = 'faca'
    FOR = 'PARA'
    SWITCH = 'ESCOLHA'
    CASE = 'CASO'
    DEFAULT = 'FALTA'
    BREAK = 'QUEBRAR'
    CONTINUE = 'CONTINUAR'

    # Operadores
    PLUS = 'SOMAR'
    MINUS = 'SUBTRAIR'
    MULTIPLY = 'MULTIPLICAR'
    DIVIDE = 'DIVIDIR'
    MODULE = 'MODULO'
    POW = 'POTENCIAR'
    SEPARATE = 'SEPARAR'
    ASSIGN = 'ATRIBUIR'

    LESS_THAN = 'MENOR'
    GREAT_THAN = 'MAIOR'
    LESS_EQUAL = 'MENOR_IGUAL'
    GREAT_EQUAL = 'MAIOR_IGUAL'
    EQUAL = 'IGUAL'
    NO_EQUAL = 'DIFERENTE'
    AND = 'E'
    OR = 'OU'
    NOT = 'NAO'

    # Grupos de dados
    ISOLATE = 'ISOLAR'
    ALINE = 'ALINHAR'
    KEY = 'CHAVE'

    # Erro de sintaxe
    ERROR = 'Erro'
    SYNTAXERROR = 'Erro De Sintaxe'
    VALUEERROR = 'Erro De Valor'

    # Lista de Tipo de Dados
    _TYPE_DATA = {
        INTEGER: 'inteiro',
        FLOAT: 'decimal',
        BOOLEAN: 'binario',
        STRING: 'texto',
    }

    # Lista de Operadores
    _OPERATORS = {
        # todos operadores serão definidos aqui
        # token: { order: 0...9, fat: bool uni: bool }
    }

    # Lista de Funções
    _FUNCTIONS = {
        # todas funções serão definidos aqui
        # token: (value: str)
    }

    # Lista de grupo de àrvores
    _GROUPS = {
        # todos grupos serão definidos aqui
        # token: (value: str)
    }

    # Lista de blocos de código
    _BLOCKS = {
        # todos blocos serão definidos aqui
        # token: (value: str)
    }

    # Todos os Tokens
    _TOKENS = {
        # tipo de dados
        'inteiro': INTEGER,
        'decimal': FLOAT,
        'binario': BOOLEAN,
        'texto': STRING,

        # Identificadores estáticos
        'falso': BOOLEAN,
        'verdade': BOOLEAN,
        'nada': NULL,

        # Condicionais
        'se': IF,
        'senao': ELSE,
        'escolha': SWITCH,
        'caso': CASE,
        'contrario': DEFAULT,

        # Loops
        'faca': DO,
        'enquanto': WHILE,
        'para': FOR,
        'quebrar': BREAK,
        'continuar': CONTINUE,

        # Operadores
        '+': PLUS,
        '-': MINUS,
        '*': MULTIPLY,
        '/': DIVIDE,
        '%': MODULE,
        '**': POW,
        ',': SEPARATE,

        '=': ASSIGN,
        '<': LESS_THAN,
        '<=': LESS_THAN,
        '>': GREAT_THAN,
        '>=': GREAT_EQUAL,
        '==': EQUAL,
        '!=': NO_EQUAL,
        'e': AND,
        'ou': OR,
        'nao': NOT,

        # Caracter de Grupos
        '(': ISOLATE + '_0',
        ')': ISOLATE + '_1',
        '[': KEY + '_0',
        ']': KEY + '_1',
        '{': ALINE + '_0',
        '}': ALINE + '_1',

        # Caracter de fim de instrução
        '\n': END, ';': END,
    }

    def __init__(self, tpye: str, value: object, line: tuple[int, int] = (0, 0)):
        self._type = tpye
        self._value = value
        self._line = line

    @staticmethod
    def register(feature: dict):
        match feature['type']:
            case Token.OPERATOR:
                if not feature['token'] in Token._OPERATORS:
                    if 'value' in feature:
                        Token._TOKENS[feature['value']] = feature['token']
                    Token._OPERATORS[feature['token']] = {
                        'order': feature['order'],
                        'fat': feature['fat'] if 'fat' in feature else False,
                        'uni': feature['uni'] if 'uni' in feature else False,
                    }
                    return True

            case Token.FUNCTION:
                feature['token'] = feature['type'] + '_' + feature['value']
                if feature['token'] not in Token._FUNCTIONS:
                    Token._FUNCTIONS[feature['token']] = feature['token']
                    Token._TOKENS[feature['value']] = feature['token']
                    return True

            case Token.GROUP:
                if feature['token'] + '_0' not in Token._GROUPS:
                    Token._GROUPS[feature['token'] + '_0'] = feature['token']
                    Token._OPERATORS[feature['token'] + '_1'] = {
                        'order': 0,
                        'fat': feature['fat'] if 'fat' in feature else False,
                        'uni': feature['uni'] if 'uni' in feature else False,
                    }
                    return True

            case Token.BLOCK:
                if feature['token'] not in Token._BLOCKS:
                    Token._BLOCKS[feature['token']] = Token.token(feature['token'])
                    return True

        return False

    @staticmethod
    def is_value(token_type: str) -> bool:
        if token_type in Token._TYPE_DATA: return True
        if token_type in Token.NULL: return True
        if token_type in Token.ID: return True

        return False

    @staticmethod
    def is_operator(token_type: str, order: int, fat=None, uni=None) -> bool:
        if token_type not in Token._OPERATORS: return False
        if order and Token._OPERATORS[token_type]['order'] != order:
            if Token._OPERATORS[token_type]['order']:
                return False
        if fat is not None and Token._OPERATORS[token_type]['fat'] != fat: return False
        if uni is not None and Token._OPERATORS[token_type]['uni'] != uni: return False

        return True

    @staticmethod
    def operator_order_max():
        return Token._OPERATOR_ORDER_MAX

    @staticmethod
    def char_max():
        return Token._CHAR_MAX

    @staticmethod
    def is_function(token_type: str) -> bool:
        return token_type in Token._FUNCTIONS

    @staticmethod
    def is_group(token_type: str, index=0, fat=None, uni=None):
        if ((token_type in Token._GROUPS and token_type[-1] == str(index)) or
            (token_type in Token._OPERATORS and token_type[-1] == str(index))):
            if fat is not None and Token._OPERATORS[token_type[:-1] + '1']['fat'] != fat:
                return None
            if uni is not None and Token._OPERATORS[token_type[:-1] + '1']['uni'] != uni:
                return None

            return Token(token_type[:-2], [
                Token.token(token_type[:-1] + '0'),
                Token.token(token_type[:-1] + '1'),
            ])
        return None

    @staticmethod
    def is_block(token_type: str):
        return token_type in Token._BLOCKS

    @staticmethod
    def token(token_type: str):
        for token in Token._TOKENS:
            if Token._TOKENS[token] == token_type:
                return token
        return ''

    @staticmethod
    def get_type(character: str) -> str:
        if character in Token._TOKENS:
            return Token._TOKENS[character]
        return ''

    @property
    def type(self) -> str:
        return self._type

    @property
    def value(self) -> object:
        return self._value

    @property
    def line(self) -> tuple[int, int]:
        return self._line

    def __repr__(self):
        return f'Token({self.type}, {repr(self.value)})'