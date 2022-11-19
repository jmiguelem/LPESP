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
pilaSaltos = []
contadorAvail = 0
direccionAvail = 20000
pCuadruplos = Cuadruplos()
contadorCuadruplos = 0

#Contadores de Variables Globales
cge = 0; cgf = 0; cgt = 0; cgl = 0

#Contadores de Constantes
cce = 0; ccf= 0; cct = 0; ccl = 0

# ESTRUCTURA DEL PROGRAMA
def p_inicio(p):
    '''inicio : LPESP ID pn_crear_directorio PUNTOCOMA VARS DOSPUNTOS pn_crear_tabla_variables bloque_variables ESP DOSPUNTOS bloque PSE PUNTOCOMA pn_terminar_programa'''

def p_bloque_variables(p):
    '''bloque_variables : variables
                        | empty '''

# # ----- GRAMATICA Y PNS DE VARIABLES -----

def p_variables(p):
    '''variables : VAR tipo_variable id_variable PUNTOCOMA variables2'''

def p_variables2(p):
    '''variables2 : VAR tipo_variable id_variable PUNTOCOMA variables2
                | empty'''

def p_id_variable(p):
    '''id_variable : ID pn_agrega_variable id_variable2
                    | empty'''

def p_id_variable2(p):
    '''id_variable2 : COMA ID pn_agrega_variable id_variable2
                    | empty'''


def p_tipo_variable(p):
    '''tipo_variable : ENTERO
                    | FLOTANTE
                    | TEXTO
                    | LOGICO'''

    global tipoVariable
    tipoVariable = p[1]

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



# ----- BLOQUE DE CODIGO -----
def p_bloque(p):
    '''bloque : estatutos
                | empty'''



# ----- ESTATUTOS PERMITIDOS -----
def p_estatutos(p):
    '''estatutos : estatuto estatutos
                | empty'''

def p_estatuto(p):
    '''estatuto : asigna
                | imprimir
                | lectura
                | si
                | ciclo_dowhile
                | ciclo_while'''

# ----- GRAMATICA Y PNS DE ASSIGN -----
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
        global contadorAvail, contadorCuadruplos
        contadorCuadruplos += 1
        pilaCuadruplos.append([operador, op_der, "", op_izq])
        pCuadruplos.generarCuadruplo(contadorCuadruplos, operador, dir_der, "", dir_izq)
        print(f"Se genero cuadruplo {pilaCuadruplos[-1]}")
        
    else : 
        print(f"Error - Asignacion invalida")
        quit()


# ----- GRAMATICA Y PNS DE PRINT -----
def p_imprimir(p):
    '''imprimir : IMPRIME PARIZQ imprimir_par PARDER PUNTOCOMA'''

def p_imprimir_par(p):
    '''imprimir_par : expr pn_imprimir imprimir_exp'''

def p_imprimir_exp(p):
    '''imprimir_exp : COMA imprimir_par
                    | empty'''

def p_pn_imprimir(p):
    '''pn_imprimir : empty'''
    global contadorCuadruplos
    contadorCuadruplos += 1
    pilaCuadruplos.append(["IMPRIME", "", "", pilaOper.pop()])
    pCuadruplos.generarCuadruplo(contadorCuadruplos, "IMPRIME", "", "", pilaDir.pop())
    pilaTipos.pop()
    print(f"Se genero cuadruplo {pilaCuadruplos[-1]}")

# ----- GRAMATICA Y PNS DE READ -----
def p_lectura(p):
    '''lectura : LEER PARIZQ lectura_par PARDER PUNTOCOMA'''

def p_lectura_par(p):
    '''lectura_par : ID pn_lectura lectura_exp'''

def p_lectura_exp(p):
    '''lectura_exp : COMA lectura_par
                | empty'''

def p_pn_lectura(p):
    '''pn_lectura : empty'''
    global contadorCuadruplos
    contadorCuadruplos += 1
    direc = directorio.directorio[funcionActual]
    tabla = direc[1]
    variable = tabla.verificarVariable(p[-1])
    dir_variable = tabla.regresarDireccion(p[-1])
    pilaCuadruplos.append(["LEER", "", "", p[-1]])
    pCuadruplos.generarCuadruplo(contadorCuadruplos, "LEER", "", "", dir_variable)
    print(f"Se genero cuadruplo {pilaCuadruplos[-1]}")
    



# ----- GRAMATICA Y PNS DE IF -----
def p_si(p):
    '''si : SI PARIZQ megaexpr pn_agregar_exp_if PARDER DOSPUNTOS estatutos si2 FIN PUNTOCOMA pn_salida_if'''

def p_si2(p):
    ''' si2 : SINO DOSPUNTOS pn_generar_goto estatutos
            | empty'''

def p_pn_agregar_exp_if(p):
    '''pn_agregar_exp_if : empty'''
    print(f"\nPila SALTOS: {pilaSaltos}")
    condicion = pilaOper.pop()
    tipo_condicion = pilaTipos.pop()
    dir = pilaDir.pop()
    if tipo_condicion != "logico":
        print("Error - Expresion no es logica")
        quit()
    global contadorCuadruplos
    contadorCuadruplos += 1
    pilaCuadruplos.append(["GOTOF", condicion, "", "PENDIENTE"])
    pCuadruplos.generarCuadruplo(contadorCuadruplos, "GOTOF", dir, "", "PENDIENTE")
    print(f"Se genero cuadruplo {pilaCuadruplos[-1]}")
    pilaSaltos.append(contadorCuadruplos)
    print(f"Pila SALTOS: {pilaSaltos}")

def p_pn_salida_if(p):
    '''pn_salida_if : empty'''
    print(f"\nPila SALTOS: {pilaSaltos}")
    pendiente = pilaSaltos.pop()
    pilaCuadruplos[pendiente - 1][3] = contadorCuadruplos + 1
    pCuadruplos.rellenarSalto(pendiente, contadorCuadruplos + 1)
    print(f"Se relleno cuadruplo {pilaCuadruplos[pendiente - 1]}")
    print(f"Pila SALTOS: {pilaSaltos}")

def p_pn_generar_goto(p):
    '''pn_generar_goto : empty'''
    print(f"\nPila SALTOS: {pilaSaltos}")
    falso = pilaSaltos.pop()
    global contadorCuadruplos
    contadorCuadruplos += 1
    pilaCuadruplos.append(["GOTO", "", "", "PENDIENTE"])
    pCuadruplos.generarCuadruplo(contadorCuadruplos, "GOTO", "", "", "PENDIENTE")
    print(f"Se genero cuadruplo {pilaCuadruplos[-1]}")
    pilaSaltos.append(contadorCuadruplos)
    pilaCuadruplos[falso-1][3] = contadorCuadruplos+1
    pCuadruplos.rellenarSalto(falso, contadorCuadruplos+1)
    print(f"Se relleno cuadruplo {pilaCuadruplos[falso-1]}")
    print(f"Pila SALTOS: {pilaSaltos}")

# ----- GRAMATICA Y PNS DE DOWHILE -----
def p_ciclo_dowhile(p):
    '''ciclo_dowhile : EJECUTA DOSPUNTOS pn_salto_dowhile estatutos FIN MIENTRAS PARIZQ megaexpr PARDER pn_retorno_dowhile PUNTOCOMA'''

def p_pn_salto_dowhile(p):
    '''pn_salto_dowhile : empty'''
    global contadorCuadruplos
    pilaSaltos.append(contadorCuadruplos + 1)
    print(f"\nSe guardo salto de dowhile: {pilaSaltos}")
    

def p_pn_retorno_dowhile(p):
    '''pn_retorno_dowhile : empty'''
    print(f"\nPila SALTOS: {pilaSaltos}")
    retorno = pilaSaltos.pop()
    condicion = pilaOper.pop()
    tipo_condicion = pilaTipos.pop()
    dir = pilaDir.pop()
    if tipo_condicion != "logico":
        print("Error - Expresion no es logica")
        quit()
    global contadorCuadruplos
    contadorCuadruplos += 1
    pilaCuadruplos.append(["GOTOT", condicion, "", retorno])
    pCuadruplos.generarCuadruplo(contadorCuadruplos, "GOTOT", dir, "", retorno)
    print(f"Se genero cuadruplo {pilaCuadruplos[-1]}")
    print(f"Pila SALTOS: {pilaSaltos}")

# ----- GRAMATICA Y PNS DE WHILE -----
def p_ciclo_while(p):
    '''ciclo_while : MIENTRAS PARIZQ pn_salto_exp megaexpr pn_agregar_exp_while PARDER DOSPUNTOS estatutos FIN pn_salida_while PUNTOCOMA'''

def p_pn_salto_exp(p):
    '''pn_salto_exp : empty'''
    global contadorCuadruplos
    pilaSaltos.append(contadorCuadruplos + 1)
    print(f"\nSe guardo salto de while: {pilaSaltos}")
    

def p_pn_agregar_exp_while(p):
    '''pn_agregar_exp_while : empty'''
    print(f"\nPila SALTOS: {pilaSaltos}")
    condicion = pilaOper.pop()
    tipo_condicion = pilaTipos.pop()
    dir = pilaDir.pop()
    if tipo_condicion != "logico":
        print("Error - Expresion no es logica")
        quit()
    global contadorCuadruplos
    contadorCuadruplos += 1
    pilaCuadruplos.append(["GOTOF", condicion, "", "PENDIENTE"])
    pCuadruplos.generarCuadruplo(contadorCuadruplos, "GOTOF", dir, "", "PENDIENTE")
    print(f"Se genero cuadruplo {pilaCuadruplos[-1]}")
    pilaSaltos.append(contadorCuadruplos)
    print(f"Pila SALTOS: {pilaSaltos}")

def p_pn_salida_while(p):
    '''pn_salida_while : empty'''
    print(f"\nPila SALTOS: {pilaSaltos}")
    falso = pilaSaltos.pop()
    salto_exp = pilaSaltos.pop()

    global contadorCuadruplos
    contadorCuadruplos += 1

    pilaCuadruplos.append(["GOTO", "", "", salto_exp])
    pCuadruplos.generarCuadruplo(contadorCuadruplos, "GOTO", "", "", salto_exp)
    print(f"Se genero cuadruplo {pilaCuadruplos[-1]}")
    

    pilaCuadruplos[falso-2][3] = contadorCuadruplos+1
    pCuadruplos.rellenarSalto(falso, contadorCuadruplos+1)
    print(f"Se relleno cuadruplo {pilaCuadruplos[falso-2]}")
    print(f"Pila SALTOS: {pilaSaltos}")


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
    print(f"\n Cuadruplos Generados \n")
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
    if p[-1] == "falso":
        pilaDir.append(tablaConstantes.regresarDireccion("FALSO"))
    else:
        pilaDir.append(tablaConstantes.regresarDireccion("VERDADERO"))
    pilaOper.append(p[-1])
    pilaTipos.append("logico")
        
    

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
            global contadorCuadruplos
            contadorCuadruplos += 1
            resultado = "t" + str(contadorAvail)
            pilaDir.append(direccionAvail + contadorAvail)
            contadorAvail = contadorAvail + 1
            pilaCuadruplos.append([operador, op_izq, op_der, resultado])
            pilaOper.append(resultado)
            pilaTipos.append(Semantica.obtener_token(tipo_resultado))
            pCuadruplos.generarCuadruplo(contadorCuadruplos, operador, dir_izq, dir_der, pilaDir[-1])
            print(f"Se genero cuadruplo {pilaCuadruplos[-1]}")
            
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
            global contadorCuadruplos
            contadorCuadruplos += 1
            resultado = "t" + str(contadorAvail)
            pilaDir.append(direccionAvail + contadorAvail)
            contadorAvail = contadorAvail + 1
            pilaCuadruplos.append([operador, op_izq, op_der, resultado])
            pilaOper.append(resultado)
            pilaTipos.append(Semantica.obtener_token(tipo_resultado))
            pCuadruplos.generarCuadruplo(contadorCuadruplos, operador, dir_izq, dir_der, pilaDir[-1])
            print(f"Se genero cuadruplo {pilaCuadruplos[-1]}")
            
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
            global contadorCuadruplos
            contadorCuadruplos += 1
            resultado = "t" + str(contadorAvail)
            pilaDir.append(direccionAvail + contadorAvail)
            contadorAvail = contadorAvail + 1
            pilaCuadruplos.append([operador, op_izq, op_der, resultado])
            pilaOper.append(resultado)
            pilaTipos.append(Semantica.obtener_token(tipo_resultado))
            pCuadruplos.generarCuadruplo(contadorCuadruplos, operador, dir_izq, dir_der, pilaDir[-1])
            print(f"Se genero cuadruplo {pilaCuadruplos[-1]}")
            
        else:
            print("Error - Tipo de dato erroneo")
            quit()

def p_pn_sacar_poper1(p):
    '''pn_sacar_poper1 : empty'''
    print("\n")
    print(f"Tipos: {pilaTipos}")
    print(f"Operandos: {pilaOper}")
    print(f"Operadores: {pOper}")
    print(f"Direccion : {pilaDir}")
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
            global contadorCuadruplos
            contadorCuadruplos += 1
            resultado = "t" + str(contadorAvail)
            pilaDir.append(direccionAvail + contadorAvail)
            contadorAvail = contadorAvail + 1
            pilaCuadruplos.append([operador, op_izq, op_der, resultado])
            pilaOper.append(resultado)
            pilaTipos.append(Semantica.obtener_token(tipo_resultado))
            pCuadruplos.generarCuadruplo(contadorCuadruplos ,operador, dir_izq, dir_der, pilaDir[-1])
            print(f"Se genero cuadruplo {pilaCuadruplos[-1]}")
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
code = open("ejercicioWhile", 'r')
data = str(code.read())
yacc.yacc()
yacc.parse(data)
lexer = lexico.lexer
lexer.input(data)
#for tok in lexer:
    #print(tok)
