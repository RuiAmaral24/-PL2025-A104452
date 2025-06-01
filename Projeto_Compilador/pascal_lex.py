import ply.lex as lex
import re

# Lista de tokens
tokens = [
    # Literais e identificadores
    'ID', 'NUMBER', 'REAL', 'STRING_LITERAL',

    # Operadores
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'ASSIGN', 'EQ', 'NE', 'LT', 'LE', 'GT', 'GE',

    # Delimitadores
    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET',
    'COLON', 'SEMICOLON', 'COMMA', 'DOT', 'DOTDOT',

    # Outras palavras
    'PROGRAM', 'VAR', 'BEGIN', 'END',
    'INTEGER', 'REAL_TYPE', 'STRING_TYPE', 'BOOLEAN',
    'READLN', 'WRITELN', 'WRITE',
    'IF', 'THEN', 'ELSE',
    'FOR', 'TO', 'DOWNTO', 'DO',
    'WHILE', 'FUNCTION',
    'DIV', 'MOD',
    'TRUE', 'FALSE',
    'ARRAY', 'OF',
    'NOT', 'AND', 'OR'
]

# Operadores
t_PLUS       = r'\+'
t_MINUS      = r'-'
t_TIMES      = r'\*'
t_DIVIDE     = r'/'
t_ASSIGN     = r':='
t_EQ         = r'='
t_NE         = r'<>'
t_LT         = r'<'
t_LE         = r'<='
t_GT         = r'>'
t_GE         = r'>='

# Delimitadores
t_LPAREN     = r'\('
t_RPAREN     = r'\)'
t_LBRACKET   = r'\['
t_RBRACKET   = r'\]'
t_COLON      = r':'
t_SEMICOLON  = r';'
t_COMMA      = r','
t_DOTDOT     = r'\.\.'
t_DOT        = r'\.'

# Ignorar espaços e tabs
t_ignore = ' \t'

# Comentários
def t_COMMENT(t):
    r'\{[^}]*\}'
    pass

# Números reais
def t_REAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# Números inteiros
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Strings entre apóstrofes
def t_STRING_LITERAL(t):
    r'\'([^\\\n]|(\\.))*?\''
    t.value = t.value[1:-1]
    return t

# Estrutura do programa
def t_PROGRAM(t):     r'\bprogram\b';     return t
def t_FUNCTION(t):    r'\bfunction\b';    return t
def t_VAR(t):         r'\bvar\b';         return t
def t_BEGIN(t):       r'\bbegin\b';       return t
def t_END(t):         r'\bend\b';         return t

# Tipos de dados
def t_INTEGER(t):     r'\binteger\b';     return t
def t_REAL_TYPE(t):   r'\breal\b';        return t
def t_STRING_TYPE(t): r'\bstring\b';      return t
def t_BOOLEAN(t):     r'\bboolean\b';     return t

# Constantes booleanas
def t_TRUE(t):        r'\btrue\b';        return t
def t_FALSE(t):       r'\bfalse\b';       return t

# Controlos de fluxo
def t_IF(t):          r'\bif\b';          return t
def t_THEN(t):        r'\bthen\b';        return t
def t_ELSE(t):        r'\belse\b';        return t
def t_FOR(t):         r'\bfor\b';         return t
def t_TO(t):          r'\bto\b';          return t
def t_DOWNTO(t):      r'\bdownto\b';      return t
def t_DO(t):          r'\bdo\b';          return t
def t_WHILE(t):       r'\bwhile\b';       return t

# Operadores lógicos e aritméticos especiais
def t_DIV(t):         r'\bdiv\b';         return t
def t_MOD(t):         r'\bmod\b';         return t
def t_NOT(t):         r'\bnot\b';         return t
def t_AND(t):         r'\band\b';         return t
def t_OR(t):          r'\bor\b';          return t

# Arrays e estruturas
def t_ARRAY(t):       r'\barray\b';       return t
def t_OF(t):          r'\bof\b';          return t

# Entrada/saída
def t_READLN(t):      r'\breadln\b';      return t
def t_WRITELN(t):     r'\bwriteln\b';     return t
def t_WRITE(t):       r'\bwrite\b';       return t

# Identificadores (o que sobra)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# Novas linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Erros léxicos
def t_error(t):
    raise SyntaxError(f"Caractere ilegal '{t.value[0]}' (linha {t.lineno})")

# Construir o lexer
lexer = lex.lex(reflags=re.IGNORECASE)
