import ply.yacc as yacc
import lexico
from directorio import Directorio
tokens = lexico.tokens




# ESTRUCTURA DEL PROGRAMA
def p_inicio(p):
    '''inicio : LPESP ID pn_crear_directorio PUNTOCOMA VARS DOSPUNTOS bloque_variables ESP DOSPUNTOS bloque PSE pn_terminar_programa'''

def p_bloque_variables(p):
    '''bloque_variables : pn_crear_tabla_variables variables 
                        | empty '''

def p_bloque(p):
    '''bloque : estatutos
                | empty'''

# VARIABLES
def p_variables(p):
    '''variables : variable variables
                | empty'''

def p_variable(p):
    '''variable : VAR tipo_variable ID pn_agrega_variable PUNTOCOMA'''

def p_tipo_variable(p):
    '''tipo_variable : ENTERO
                    | FLOTANTE
                    | TEXTO
                    | LOGICO'''

    global tipoVariable
    tipoVariable = p[1]

# ESTATUTOS DISPONIBLES
def p_estatutos(p):
    '''estatutos : estatuto estatutos
                | empty'''

def p_estatuto(p):
    '''estatuto : asigna
                | si'''

def p_si(p):
    '''si : SI PARIZQ expr PARDER estatuto si2'''

def p_si2(p):
    ''' si2 : SINO estatuto
            | empty'''

def p_asigna(p):
    '''asigna : ID IGUAL expr PUNTOCOMA'''

# EXPRESIONES
def p_expr(p):
    '''expr : expr OPERLOGICO gigaexpr
            | gigaexpr'''

def p_gigaexpr(p):
    '''gigaexpr : megaexpr OPERREL megaexpr
            | megaexpr'''

def p_megaexpr(p):
    '''megaexpr : megaexpr OPER1 term
            | term'''

def p_term(p):
    '''term : term OPER2 factor
            | factor'''

def p_factor(p):
    '''factor : CTEENT
            | CTEFLOT
            | CTETEXTO
            | PARIZQ expr PARDER
            | ID
            | FALSO
            | VERDADERO'''

# PUNTOS NEURALGICOS

# ESTRUCTURA DEL PROGRAMA

def p_pn_crear_directorio(p):
    '''pn_crear_directorio : empty'''

    #Se crean variables globales
    global directorio
    global nombrePrograma
    global funcionActual

    #Se crea el directorio de funciones
    directorio = Directorio()

    #Actualiza las variables con el id del programa
    nombrePrograma = p[-1]
    funcionActual = nombrePrograma

    #Se agrega la funcion de global
    directorio.agregarNuevaFuncion(nombrePrograma, "void")

def p_pn_terminar_programa(p):
    '''pn_terminar_programa : empty'''
    directorio.eliminarTablaVariables(nombrePrograma)
    directorio.eliminarFuncion(nombrePrograma)

# VARIABLES

def p_pn_crear_tabla_variables(p):
    '''pn_crear_tabla_variables : empty'''
    directorio.crearTablaVariables(nombrePrograma)
    print("Se creo tabla")

def p_pn_agrega_variable(p):
    '''pn_agrega_variable : empty'''
    directorio.directorio[nombrePrograma][1].crear(p[-1], tipoVariable)

# EXTRA
def p_error(p):
    print(f"Error de sintaxis en {p}")
    exit()

def p_empty(p):
    '''empty : '''
    pass
    


# Ejecutar Codigo
code = open("prueba", 'r')
data = str(code.read())
yacc.yacc()
yacc.parse(data)
lexer = lexico.lexer
lexer.input(data)
#for tok in lexer:
    #print(tok)
