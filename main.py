import ply.yacc as yacc
import lexico
from directorio import Directorio
from semantica import Semantica
from cuadruplos import Cuadruplos 
from directorio import Constantes
tokens = lexico.tokens

pilaTipos = []
pilaOper = []
pilaDir = []
pOper = [""]
pilaCuadruplos = []
contadorAvail = 0
direccionAvail = 20000
pCuadruplos = Cuadruplos()

#Contadores de Variables Globales
global cge, cgf, cgt, cgl
cge = 0; cgf = 0; cgt = 0; cgl = 0

#Contadores de Constantes
global cce, ccf, cct, ccl
cce = 0; ccf= 0; cct = 0; ccl = 0

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
    '''asigna : ID pn_agregar_id IGUAL pn_agregar_igual expr pn_asignar PUNTOCOMA'''

def p_pn_agregar_igual(p):
    '''pn_agregar_igual :  empty'''
    pOper.append(p[-1])

def p_pn_asignar(p):
    '''pn_asignar : empty'''
    tipo_der = pilaTipos.pop()
    tipo_izq = pilaTipos.pop()
    operador = pOper.pop()
    op_der = pilaOper.pop()
    op_izq = pilaOper.pop()
    dir_izq = pilaDir.pop()
    dir_der = pilaDir.pop()

    if tipo_izq == tipo_der:
        global contadorAvail
        pilaCuadruplos.append([operador, op_der, "", op_izq])
        pCuadruplos.generarCaudruplo(operador, dir_der, "", dir_izq)
        
    else : 
        print(f"Error - Asignacion invalida")
        quit()


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
    pCuadruplos.generarCaudruplo("IMPRIME", "", "", pilaDir.pop())
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
    '''megaexpr2 : OPERLOGICO pn_agregar_oper megaexpr pn_sacar_poperLog
                | OPERREL pn_agregar_oper megaexpr pn_sacar_poperLog
                | expr pn_sacar_poperLog
                | empty'''
def p_expr(p):
    '''expr : exp comparacion pn_sacar_poperLog'''

def p_comparacion(p):
    '''comparacion : OPERREL pn_agregar_oper comparacion2
            | empty'''

def p_comparacion2(p):
    '''comparacion2 : exp pn_sacar_poperRel'''

def p_exp(p):
    '''exp : term operador'''

def p_operador(p):
    '''operador : OPER1 pn_agregar_oper term pn_sacar_poper1 operador
            | empty'''

def p_term(p):
    '''term : factor term2 '''

def p_term2(p):
    '''term2 : OPER2 pn_agregar_oper factor pn_sacar_poper2 term2
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
    global tablaConstantes 

    #Se crea el directorio de funciones
    directorio = Directorio()

    #Se crea la tabla de constantes
    tablaConstantes = Constantes()

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
    tablaConstantes.imprimir()
    print(f"Cuadruplos Generados \n")
    contador = 1
    for cuadruplo in pilaCuadruplos:
        print(f"{contador} : {cuadruplo}")
        contador += 1
    pCuadruplos.imprimir()

# VARIABLES

def p_pn_crear_tabla_variables(p):
    '''pn_crear_tabla_variables : empty'''
    directorio.crearTablaVariables(nombrePrograma)
    #print("Se creo tabla")

def p_pn_agrega_variable(p):
    '''pn_agrega_variable : empty'''
    global cge, cgf, cgl, cgt
    if tipoVariable == "entero":
        cge += 1
        direccion = 1000 + cge
    elif tipoVariable == "flotante":
        cgf += 1
        direccion = 5000 + cgf
    elif tipoVariable == "texto":
        cgt += 1
        direccion = 9000 + cgt
    elif tipoVariable == "logico":
        cgl += 1
        direccion = 13000 + cgl
    directorio.directorio[nombrePrograma][1].crear(p[-1], tipoVariable, direccion)
    print("VARIABLES GLOBALES",cge,cgf,cgt, cgl)
    


# EXPRESIONES

#IDS Y CTES
def p_pn_agregar_id(p):
    '''pn_agregar_id : empty'''
    directorio.directorio[funcionActual][1].verificarVariable(p[-1])
    pilaOper.append(p[-1])
    tipo = directorio.directorio[funcionActual][1].regresarTipo(p[-1])
    pilaTipos.append(tipo)
    direccion = directorio.directorio[funcionActual][1].regresarDireccion(p[-1])
    pilaDir.append(direccion)


def p_pn_agregar_ENT(p):
    '''pn_agregar_ENT : empty'''
    global cce
    global tablaConstantes
    cce += 1
    cce += tablaConstantes.agregarConstante(p[-1], cce, 0)
    pilaOper.append(p[-1])
    pilaTipos.append("entero")
    pilaDir.append(tablaConstantes.regresarDireccion(p[-1]))
    

def p_pn_agregar_FLOT(p):
    '''pn_agregar_FLOT : empty'''
    global ccf
    global tablaConstantes
    ccf += 1
    ccf += tablaConstantes.agregarConstante(p[-1], ccf, 1)
    pilaOper.append(p[-1])
    pilaTipos.append("flotante")
    pilaDir.append(tablaConstantes.regresarDireccion(p[-1]))

def p_pn_agregar_TEXTO(p):
    '''pn_agregar_TEXTO : empty'''
    global cct
    global tablaConstantes
    cct += 1
    cct += tablaConstantes.agregarConstante(p[-1], cct, 2)
    pilaOper.append(p[-1])
    pilaTipos.append("texto")
    pilaDir.append(tablaConstantes.regresarDireccion(p[-1]))

def p_pn_agregar_LOGICO(p):
    '''pn_agregar_LOGICO : empty'''
    global ccl
    global constantes
    ccl += 1
    ccl += tablaConstantes.agregarConstante(p[-1], ccl, 3)
    pilaOper.append(p[-1])
    pilaTipos.append("logico")
    pilaDir.append(tablaConstantes.regresarDireccion(p[-1]))

# AGREGAR OPERADORES
def p_pn_agregar_oper(p):
    '''pn_agregar_oper : empty'''
    pOper.append(p[-1])



# SACAR OPERADORES
def p_pn_sacar_poperLog(p):
    '''pn_sacar_poperLog : empty'''
    print("\n")
    print(f"Tipos: {pilaTipos}")
    print(f"Operandos: {pilaOper}")
    print(f"Operadores: {pOper}")
    print(f"Direccion : {pilaDir}")
    if pOper[-1] == "&&" or pOper[-1] == "||":
        op_der = pilaOper.pop()
        tipo_der = Semantica.obtener_tipo(pilaTipos.pop())
        op_izq= pilaOper.pop()
        dir_der = pilaDir.pop()
        tipo_izq= Semantica.obtener_tipo(pilaTipos.pop())
        operador = pOper.pop()
        tipo_resultado = Semantica.tipo_resultado(operador, tipo_izq, tipo_der )
        dir_izq = pilaDir.pop()

        if tipo_resultado != -1:
            global contadorAvail
            global direccionAvail
            resultado = "t" + str(contadorAvail)
            pilaDir.append(direccionAvail + contadorAvail)
            contadorAvail = contadorAvail + 1
            pilaCuadruplos.append([operador, op_der, op_izq, resultado])
            pilaOper.append(resultado)
            pilaTipos.append(Semantica.obtener_token(tipo_resultado))
            pCuadruplos.generarCaudruplo(operador, dir_izq, dir_der, pilaDir[-1])
            
        else:
            print("Error - Tipo de dato erroneo")
            quit()

def p_pn_sacar_poperRel(p):
    '''pn_sacar_poperRel : empty'''
    print("\n")
    print(f"Tipos: {pilaTipos}")
    print(f"Operandos: {pilaOper}")
    print(f"Operadores: {pOper}")
    print(f"Direccion : {pilaDir}")
    if pOper[-1] == "<=" or pOper[-1] == ">=" or pOper[-1] == "<>" or pOper[-1] == "<" or pOper[-1] == ">" or pOper[-1] == "==":
        op_der = pilaOper.pop()
        tipo_der = Semantica.obtener_tipo(pilaTipos.pop())
        op_izq= pilaOper.pop()
        dir_der = pilaDir.pop()
        tipo_izq= Semantica.obtener_tipo(pilaTipos.pop())
        operador = pOper.pop()
        tipo_resultado = Semantica.tipo_resultado(operador, tipo_izq, tipo_der )
        dir_izq = pilaDir.pop()
        
        
        if tipo_resultado != -1:
            global contadorAvail
            global direccionAvail
            resultado = "t" + str(contadorAvail)
            pilaDir.append(direccionAvail + contadorAvail)
            contadorAvail = contadorAvail + 1
            pilaCuadruplos.append([operador, op_der, op_izq, resultado])
            pilaOper.append(resultado)
            pilaTipos.append(Semantica.obtener_token(tipo_resultado))
            pCuadruplos.generarCaudruplo(operador, dir_izq, dir_der, pilaDir[-1])
            
        else:
            print("Error - Tipo de dato erroneo")
            quit()

def p_pn_sacar_poper2(p):
    '''pn_sacar_poper2 : empty'''
    print("\n")
    print(f"Tipos: {pilaTipos}")
    print(f"Operandos: {pilaOper}")
    print(f"Operadores: {pOper}")
    print(f"Direccion : {pilaDir}")
    if pOper[-1] == "*" or pOper[-1] == "/":
        op_der = pilaOper.pop()
        tipo_der = Semantica.obtener_tipo(pilaTipos.pop())
        op_izq= pilaOper.pop()
        dir_der = pilaDir.pop()
        tipo_izq= Semantica.obtener_tipo(pilaTipos.pop())
        operador = pOper.pop()
        tipo_resultado = Semantica.tipo_resultado(operador, tipo_izq, tipo_der )
        dir_izq = pilaDir.pop()
        
        
        if tipo_resultado != -1:
            global contadorAvail
            global direccionAvail
            resultado = "t" + str(contadorAvail)
            pilaDir.append(direccionAvail + contadorAvail)
            contadorAvail = contadorAvail + 1
            pilaCuadruplos.append([operador, op_der, op_izq, resultado])
            pilaOper.append(resultado)
            pilaTipos.append(Semantica.obtener_token(tipo_resultado))
            pCuadruplos.generarCaudruplo(operador, dir_izq, dir_der, pilaDir[-1])
            
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
        dir_der = pilaDir.pop()
        tipo_izq= Semantica.obtener_tipo(pilaTipos.pop())
        operador = pOper.pop()
        tipo_resultado = Semantica.tipo_resultado(operador, tipo_izq, tipo_der )
        dir_izq = pilaDir.pop()
        
        if tipo_resultado != -1:
            global contadorAvail
            global direccionAvail
            resultado = "t" + str(contadorAvail)
            pilaDir.append(direccionAvail + contadorAvail)
            contadorAvail = contadorAvail + 1
            pilaCuadruplos.append([operador, op_der, op_izq, resultado])
            pilaOper.append(resultado)
            pilaTipos.append(Semantica.obtener_token(tipo_resultado))
            pCuadruplos.generarCaudruplo(operador, dir_izq, dir_der, pilaDir[-1])
        else:
            print("Error - Tipo de dato erroneo")
            quit()

#FONDOS FALSOS
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
