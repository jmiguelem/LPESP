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
    '''inicio : LPESP ID pn_crear_directorio PUNTOCOMA VARS DOSPUNTOS pn_crear_tabla_variables bloque_variables ESP DOSPUNTOS bloque PSE PUNTOCOMA pn_terminar_programa'''
    print("inicio")

def p_bloque_variables(p):
    '''bloque_variables : variables
                        | empty '''
    print("bloque_variables")

# VARIABLES

def p_variables(p):
    '''variables : VAR tipo_variable id_variable PUNTOCOMA variables2'''
    print("variables")

def p_variables2(p):
    '''variables2 : VAR tipo_variable id_variable PUNTOCOMA variables2
                | empty'''
    print("variables2")

def p_id_variable(p):
    '''id_variable : ID pn_agrega_variable id_variable2
                    | empty'''
    print("id_variable")

def p_id_variable2(p):
    '''id_variable2 : COMA ID pn_agrega_variable id_variable2
                    | empty'''
    print("id_variable2")


def p_arreglos(p): 
    '''arreglos : ARREGLO tipo_variable arreglo PUNTOCOMA'''

def p_arreglo(p):
    '''arreglo : arreglo2 arreglo
                | empty'''

def p_arreglo2(p):
    '''arreglo2 : ID CORIZQ CTEENT CORDER'''


def p_tipo_variable(p):
    '''tipo_variable : ENTERO
                    | FLOTANTE
                    | TEXTO
                    | LOGICO'''

    global tipoVariable
    tipoVariable = p[1]



#Codigo
def p_bloque(p):
    '''bloque : estatutos
                | empty'''



# ESTATUTOS DISPONIBLES
def p_estatutos(p):
    '''estatutos : estatuto estatutos
                | empty'''

def p_estatuto(p):
    '''estatuto : asigna
                | imprimir
                | si'''
# ASIGNA
def p_asigna(p):
    '''asigna : ID IGUAL expr PUNTOCOMA'''

#IMPRIME
def p_imprimir(p):
    '''imprimir : IMPRIME PARIZQ imprimir_par PARDER PUNTOCOMA'''

def p_imprimir_par(p):
    '''imprimir_par : expr pn_imprimir imprimir_exp'''

def p_imprimir_exp(p):
    '''imprimir_exp : COMA imprimir_par
                    | empty'''

def p_pn_imprimir(p):
    '''pn_imprimir : empty'''
    pilaCuadruplos.append(["IMPRIME", "", "", pilaOper.pop()])
    pilaTipos.pop()

#LEER






#SI
def p_si(p):
    '''si : SI PARIZQ expr PARDER estatuto si2'''

def p_si2(p):
    ''' si2 : SINO estatuto
            | empty'''


#CICLO





# EXPRESIONES
def p_megaexpr(p):
    '''megaexpr : expr megaexpr2'''

def p_megaexpr2(p):
    '''megaexpr2 : OPERLOGICO megaexpr
                        | OPERREL megaexpr
                        | expr
                        | empty'''
def p_expr(p):
    '''expr : exp comparacion'''

def p_comparacion(p):
    '''comparacion : OPERREL comparacion2
            | empty'''

def p_comparacion2(p):
    '''comparacion2 : exp'''

def p_exp(p):
    '''exp : term operador'''

def p_operador(p):
    '''operador : OPER1 pn_agregar_oper1 term pn_sacar_poper1 operador
            | empty'''

def p_term(p):
    '''term : factor term2 '''

def p_term2(p):
    '''term2 : OPER2 pn_agregar_oper2 factor pn_sacar_poper2 term2
            | empty'''
def p_factor(p):
    '''factor : PARIZQ pn_agregar_fondo_falso expr PARDER pn_checar_fondo_falso
            | var_cte'''

def p_var_cte(p):
    '''var_cte : ID pn_agregar_id
            | CTEENT pn_agregar_ENT
            | CTEFLOT pn_agregar_FLOT
            | CTETEXTO pn_agregar_TEXTO
            | FALSO pn_agregar_LOGICO
            | VERDADERO pn_agregar_LOGICO'''



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
    print("\n")
    print("Tabla de Funciones")
    directorio.imprimirTabla()
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
    directorio.directorio[funcionActual][1].verificarVariable(p[-1])
    pilaOper.append(p[-1])
    tipo = directorio.directorio[funcionActual][1].regresarTipo(p[-1])
    pilaTipos.append(tipo)

def p_pn_agrega_arreglo(p):
    '''pn_agrega_arreglo : empty'''
    print(p[-9])
    pilaOper.append[p[-1]]
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

def p_pn_agregar_oper1(p):
    '''pn_agregar_oper1 : empty'''
    pOper.append(p[-1])

def p_pn_sacar_poper2(p):
    '''pn_sacar_poper2 : empty'''
    print("\n")
    print(f"Tipos: {pilaTipos}")
    print(f"Operandos: {pilaOper}")
    print(f"Operadores: {pOper}")
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
            pilaTipos.append(Semantica.obtener_token(tipo_resultado))
        else:
            print("Error - Tipo de dato erroneo")
            quit()

def p_pn_sacar_poper1(p):
    '''pn_sacar_poper1 : empty'''
    print("\n")
    print(f"Tipos: {pilaTipos}")
    print(f"Operandos: {pilaOper}")
    print(f"Operadores: {pOper}")
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
            pilaTipos.append(Semantica.obtener_token(tipo_resultado))
        else:
            print("Error - Tipo de dato erroneo")
            quit()

def p_pn_agregar_fondo_falso(p):
    '''pn_agregar_fondo_falso : empty'''
    pOper.append(p[-1])

def p_pn_checar_fondo_falso(p):
    '''pn_checar_fondo_falso : empty'''
    if pOper[-1] == '(':
        pOper.pop() 

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
