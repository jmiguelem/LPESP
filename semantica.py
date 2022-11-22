class Semantica:
        # ENTERO   FLOTANTE    TEXTO  LOGICO
    cubo = {
        "+" : [
            [0,     1,          -1,     -1], #ENTERO
            [1,     1,          -1,     -1], #FLOTANTE
            [-1,    -1,         -1,     -1], #TEXTO
            [-1,    -1,         -1,     -1], #LOGICO
        ],
        "-" : [
            [0,     1,          -1,     -1], #ENTERO
            [1,     1,          -1,     -1], #FLOTANTE
            [-1,    -1,         -1,     -1], #TEXO
            [-1,    -1,         -1,     -1], #LOGICO
        ],
        "*" : [
            [0,     1,          -1,     -1], #ENTERO
            [1,     1,          -1,     -1], #FLOTANTE
            [-1,    -1,         -1,     -1], #TEXTO
            [-1,    -1,         -1,     -1], #LOGICO
        ],
        "/" : [
            [1,     1,          -1,     -1], #ENTERO
            [1,     1,          -1,     -1], #FLOTANTE
            [-1,    -1,         -1,     -1], #TEXTO
            [-1,    -1,         -1,     -1], #LOGICO
        ],
        "&&" : [
            [-1,    -1,         -1,     -1], #ENTERO
            [-1,    -1,         -1,     -1], #FLOTANTE
            [-1,    -1,         -1,     -1], #TEXTO
            [-1,    -1,         -1,      3], #LOGICO
        ],
        "||" : [
            [-1,    -1,         -1,     -1], #ENTERO
            [-1,    -1,         -1,     -1], #FLOTANTE
            [-1,    -1,         -1,     -1], #TEXTO
            [-1,    -1,         -1,      3], #LOGICO
        ],
        "==" : [
            [3,     3,         -1,     -1], #ENTERO
            [3,     3,         -1,     -1], #FLOTANTE
            [-1,    -1,          3,     -1], #TEXTO
            [-1,    -1,         -1,      3], #LOGICO
        ],
        "<=" : [
            [3,     3,         -1,     -1], #ENTERO
            [3,     3,         -1,     -1], #FLOTANTE
            [-1,    -1,         -1,     -1], #TEXTO
            [-1,    -1,         -1,     -1], #LOGICO
        ],
        ">=" : [
            [3,     3,         -1,     -1], #ENTERO
            [3,     3,         -1,     -1], #FLOTANTE
            [-1,    -1,         -1,     -1], #TEXTO
            [-1,    -1,         -1,     -1], #LOGICO
        ],
        "<>" : [
            [3,     3,         -1,     -1], #ENTERO
            [3,     3,         -1,     -1], #FLOTANTE
            [-1,    -1,         -1,     -1], #TEXTO
            [-1,    -1,         -1,     -1], #LOGICO
        ],
        "<" : [
            [3,     3,         -1,     -1], #ENTERO
            [3,     3,         -1,     -1], #FLOTANTE
            [-1,    -1,         -1,     -1], #TEXTO
            [-1,    -1,         -1,     -1], #LOGICO
        ],
        ">" : [
            [3,     3,         -1,     -1], #ENTERO
            [3,     3,         -1,     -1], #FLOTANTE
            [-1,    -1,         -1,     -1], #TEXTO
            [-1,    -1,         -1,     -1], #LOGICO
        ]
    }

    tipos = {
        "entero" : 0,
        "flotante" : 1, 
        "texto" : 2,
        "logico" : 3,
        "error" : -1
    }

    tokens = {
        0 : "entero",
        1 : "flotante",
        2 : "texto",
        3 : "logico"
    }

    def tipo_resultado(operador, op1, op2):
        tipo = Semantica.cubo[operador][op1][op2]
        return tipo

    def obtener_tipo(operador):
        return Semantica.tipos[operador]

    def obtener_token(tipo):
        return Semantica.tokens[tipo]
