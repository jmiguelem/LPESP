class Semantica:
        # ENTERO   FLOTANTE    CADENA  LOGICO
    cubo = {
        "+" : [
            [0,     1,          -1,     -1], #ENTERO
            [1,     1,          -1,     -1], #FLOTANTE
            [-1,    -1,         -1,     -1], #CADENA
            [-1,    -1,         -1,     -1], #LOGICO
        ],
        "-" : [
            [0,     1,          -1,     -1], #ENTERO
            [1,     1,          -1,     -1], #FLOTANTE
            [-1,    -1,         -1,     -1], #CADENA
            [-1,    -1,         -1,     -1], #LOGICO
        ],
        "*" : [
            [0,     1,          -1,     -1], #ENTERO
            [1,     1,          -1,     -1], #FLOTANTE
            [-1,    -1,         -1,     -1], #CADENA
            [-1,    -1,         -1,     -1], #LOGICO
        ],
        "/" : [
            [0,     1,          -1,     -1], #ENTERO
            [1,     1,          -1,     -1], #FLOTANTE
            [-1,    -1,         -1,     -1], #CADENA
            [-1,    -1,         -1,     -1], #LOGICO
        ],
    }

    tipos = {
        "entero" : 0,
        "flotante" : 1, 
        "cadena" : 2,
        "logico" : 3,
        "error" : -1
    }

    def tipo_resultado(operador, op1, op2):
        tipo = Semantica.cubo[operador][op1][op2]
        return tipo

    def obtener_tipo(operador):
        return Semantica.tipos[operador]