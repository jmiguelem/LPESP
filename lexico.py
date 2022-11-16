import ply.lex as lex

# RESERVADAS
palabras_reservadas = {
    'LpEsp': 'LPESP',
    'Esp': 'ESP',
    'Variables': 'VARS',
    'Funciones': 'FUNCS',
    'func' : 'FUNC',
    'var': 'VAR',
    'arreglo' : 'ARREGLO',
    'matriz' : 'MATRIZ',
    'entero': 'ENTERO',
    'flotante': 'FLOTANTE',
    'texto': 'TEXTO',
    'logico': 'LOGICO',
    'verdadero': 'VERDADERO',
    'falso': 'FALSO',
    'si': 'SI',
    'sino': 'SINO',
    'mientras': 'MIENTRAS',
    'imprime': 'IMPRIME',
    'fin' : 'FIN',
    'Pse' : 'PSE'
}

# TOKENS
tokens = [
    'PARIZQ',
    'PARDER',
    'LLAVEIZQ',
    'LLAVEDER',
    'CORIZQ',
    'CORDER',
    'OPER1',
    'OPER2',
    'OPERLOGICO',
    'ID',
    'CTEENT',
    'CTEFLOT',
    'CTETEXTO',
    'OPERREL',
    'COMA',
    'PUNTOCOMA',
    'PUNTO',
    'IGUAL',
    'DOSPUNTOS'
] 

# TOKENS FINALES
tokens = tokens + list(palabras_reservadas.values())

# EXPRESIONES REGULARES
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_LLAVEIZQ = r'\{'
t_LLAVEDER = r'\}'
t_CORIZQ = r'\['
t_CORDER = r'\]'
t_OPER1 = r'\+|\-'
t_OPER2 = r'\*|\/'
t_OPERLOGICO = r'(\&\&|\|\|)'
t_COMA = r'\,'
t_PUNTOCOMA = r'\;'
t_PUNTO = r'\.'
t_IGUAL = r'\='
t_DOSPUNTOS = r':'
t_ignore = " \t"


def t_ID(t):
    r'[A-Za-z]([A-Za-z]|[0-9])*'
    t.type = palabras_reservadas.get(t.value, 'ID')
    return t

def t_CTEFLOT(t):
    r'[-+]?([0-9]+[.])[0-9]+'
    t.value = float(t.value)
    return t

def t_CTEENT(t):
    r'[-+]?[0-9][0-9]*'
    t.value = int(t.value)
    return t

def t_CTETEXTO(t):
    r'\'[A-Za-z_0-9$%&/\(\)\"#=\?\¿\´\+\*\-\.\,\{\}\[\]\ t]*\''
    t.type = 'CTETEXTO'
    return t

def t_OPERREL(t):
    r'<= | >= | <> | < | > | =='
    t.type = 'OPERREL'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Error lexico  {t.value[0]} en linea  {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()