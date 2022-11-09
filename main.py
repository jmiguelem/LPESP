import ply.yacc as yacc
import lexico
from directorio import Directorio
from semantica import Semantica
tokens = lexico.tokens

pilaTipos = []
pilaOper = []
pOper = []
pilaCuadruplos = []
contadorAvail = 0


# ESTRUCTURA DEL PROGRAMA
def p_inicio(p):
    '''inicio : LPESP ID pn_crear_directorio PUNTOCOMA VARS DOSPUNTOS bloque_variables ESP DOSPUNTOS bloque PSE PUNTOCOMA pn_terminar_programa'''

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
    '''megaexpr : term megaexpr2'''

def p_megaexpr2(p):
    '''megaexpr2 : OPER1 pn_agregar_oper1 term pn_sacar_poper1 megaexpr2
            | empty'''

def p_term(p):
    '''term : factor term2 '''

def p_term2(p):
    '''term2 : OPER2 pn_agregar_oper2 factor pn_sacar_poper2 term2
            | empty'''
def p_factor(p):
    '''factor : CTEENT pn_agregar_ENT
            | CTEFLOT pn_agregar_FLOT
            | CTETEXTO pn_agregar_TEXTO
            | FALSO pn_agregar_LOGICO
            | VERDADERO pn_agregar_LOGICO
            | PARIZQ expr PARDER
            | ID pn_agregar_id'''

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
    print(f"Cuadruplos Generados \n {pilaCuadruplos}")

# VARIABLES

def p_pn_crear_tabla_variables(p):
    '''pn_crear_tabla_variables : empty'''
    directorio.crearTablaVariables(nombrePrograma)
    #print("Se creo tabla")

def p_pn_agrega_variable(p):
    '''pn_agrega_variable : empty'''
    directorio.directorio[nombrePrograma][1].crear(p[-1], tipoVariable)


# EXPRESIONES

def p_pn_agregar_id(p):
    '''pn_agregar_id : empty'''
    pilaOper.append(p[-1])
    tipo = directorio.directorio[funcionActual][1].regresarTipo(p[-1])
    pilaTipos.append(tipo)
    print(pilaOper)
    print(pilaTipos)

def p_pn_agregar_ENT(p):
    '''pn_agregar_ENT : empty'''
    pilaOper.append(p[-1])
    pilaTipos.append("entero")

def p_pn_agregar_FLOT(p):
    '''pn_agregar_FLOT : empty'''
    pilaOper.append(p[-1])
    pilaTipos.append("flotante")

def p_pn_agregar_TEXTO(p):
    '''pn_agregar_TEXTO : empty'''
    pilaOper.append(p[-1])
    pilaTipos.append("texto")

def p_pn_agregar_LOGICO(p):
    '''pn_agregar_LOGICO : empty'''
    pilaOper.append(p[-1])
    pilaTipos.append("logico")

def p_pn_agregar_oper2(p):
    '''pn_agregar_oper2 : empty'''
    pOper.append(p[-1])
    print(pOper)

def p_pn_agregar_oper1(p):
    '''pn_agregar_oper1 : empty'''
    pOper.append(p[-1])
    print(pOper)

def p_pn_sacar_poper2(p):
    '''pn_sacar_poper2 : empty'''
    if pOper[-1] == "*" or pOper[-1] == "/":
        op_der = pilaOper.pop()
        tipo_der = Semantica.obtener_tipo(pilaTipos.pop())
        op_izq= pilaOper.pop()
        tipo_izq= Semantica.obtener_tipo(pilaTipos.pop())
        operador = pOper.pop()
        tipo_resultado = Semantica.tipo_resultado(operador, tipo_izq, tipo_der )
        
        if tipo_resultado != -1:
            global contadorAvail
            resultado = "t" + str(contadorAvail)
            contadorAvail = contadorAvail + 1
            pilaCuadruplos.append([operador, op_der, op_izq, resultado])
            pilaOper.append(resultado)
            pilaTipos.append(tipo_resultado)
        else:
            print("Error - Tipo de dato erroneo")
            quit()

def p_pn_sacar_poper1(p):
    '''pn_sacar_poper1 : empty'''
    if pOper[-1] == "+" or pOper[-1] == "-":
        op_der = pilaOper.pop()
        tipo_der = Semantica.obtener_tipo(pilaTipos.pop())
        op_izq= pilaOper.pop()
        tipo_izq= Semantica.obtener_tipo(pilaTipos.pop())
        operador = pOper.pop()
        tipo_resultado = Semantica.tipo_resultado(operador, tipo_izq, tipo_der )
        
        if tipo_resultado != -1:
            global contadorAvail
            resultado = "t" + str(contadorAvail)
            contadorAvail = contadorAvail + 1
            pilaCuadruplos.append([operador, op_der, op_izq, resultado])
            pilaOper.append(resultado)
            pilaTipos.append(tipo_resultado)
        else:
            print("Error - Tipo de dato erroneo")
            quit()

# Gramaticas Extra
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
