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

# Contadores de Variables Globales
cge = 0
cgf = 0
cgt = 0
cgl = 0

# Contadores de Variables Locales
cle = 0
clf = 0
clt = 0
cll = 0

# Contadores de Constantes
cce = 0
ccf = 0
cct = 0
ccl = 0

# ESTRUCTURA DEL PROGRAMA


def p_inicio(p):
    '''inicio : LPESP ID pn_crear_directorio PUNTOCOMA VARS DOSPUNTOS pn_crear_tabla_variables bloque_variables bloque_funciones ESP DOSPUNTOS bloque PSE PUNTOCOMA pn_terminar_programa'''


def p_bloque_variables(p):
    '''bloque_variables : variables
                        | empty '''

# VARIABLES


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


# Codigo
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
        global contadorAvail, contadorCuadruplos
        contadorCuadruplos += 1
        pilaCuadruplos.append([operador, op_der, "", op_izq])
        pCuadruplos.generarCuadruplo(
            contadorCuadruplos, operador, dir_der, "", dir_izq)
        print(f"Se genero cuadruplo {pilaCuadruplos[-1]}")

    else:
        print(f"Error - Asignacion invalida")
        quit()


# IMPRIME
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
    pCuadruplos.generarCuadruplo(
        contadorCuadruplos, "IMPRIME", "", "", pilaDir.pop())
    pilaTipos.pop()
    print(f"Se genero cuadruplo {pilaCuadruplos[-1]}")

# LEER


# SI
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
    pCuadruplos.generarCuadruplo(
        contadorCuadruplos, "GOTOF", dir, "", "PENDIENTE")
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
    pCuadruplos.generarCuadruplo(
        contadorCuadruplos, "GOTO", "", "", "PENDIENTE")
    print(f"Se genero cuadruplo {pilaCuadruplos[-1]}")
    pilaSaltos.append(contadorCuadruplos)
    pilaCuadruplos[falso-1][3] = contadorCuadruplos+1
    pCuadruplos.rellenarSalto(falso, contadorCuadruplos+1)
    print(f"Se relleno cuadruplo {pilaCuadruplos[falso-1]}")
    print(f"Pila SALTOS: {pilaSaltos}")


# CICLO


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

    # Se crean variables globales
    global directorio
    global nombrePrograma
    global funcionActual
    global tablaConstantes

    # Se crea el directorio de funciones
    directorio = Directorio()

    # Se crea la tabla de constantes
    tablaConstantes = Constantes()

    # Actualiza las variables con el id del programa
    nombrePrograma = p[-1]
    funcionActual = nombrePrograma

    # Se agrega la funcion de global
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
    # print("Se creo tabla")


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
    directorio.directorio[nombrePrograma][1].crear(
        p[-1], tipoVariable, direccion)
    print("VARIABLES GLOBALES", cge, cgf, cgt, cgl)


def p_pn_agrega_variable_local(p):
    global cle, clf, cll, clt
    if tipoVariableFuncion == "entero":
        cle += 1
        direccion = 10000 + cle
    elif tipoVariableFuncion == "flotante":
        clf += 1
        direccion = 50000 + clf
    elif tipoVariableFuncion == "texto":
        clt += 1
        direccion = 90000 + clt
    elif tipoVariableFuncion == "logico":
        cll += 1
        direccion = 130000 + cll

    directorio.directorio[idFuncion][1].crear(
        p[1], tipoVariableFuncion, direccion)
    directorio.contadorNuevaVariableLocal(idFuncion)
    print("VARIABLES LOCALES", cle, clf, clt, cll)


def p_pn_agrega_variable_local_param(p):
    global cle, clf, cll, clt
    if tipoParamFuncion == "entero":
        cle += 1
        direccion = 10000 + cle
    elif tipoParamFuncion == "flotante":
        clf += 1
        direccion = 50000 + clf
    elif tipoParamFuncion == "texto":
        clt += 1
        direccion = 90000 + clt
    elif tipoParamFuncion == "logico":
        cll += 1
        direccion = 130000 + cll
    directorio.directorio[idFuncion][1].crear(
        p, tipoParamFuncion, direccion)
    print("VARIABLES LOCALES", cle, clf, clt, cll)


# EXPRESIONES

# IDS Y CTES
def p_pn_agregar_id(p):
    '''pn_agregar_id : empty'''
    directorio.directorio[funcionActual][1].verificarVariable(p[-1])
    pilaOper.append(p[-1])
    tipo = directorio.directorio[funcionActual][1].regresarTipo(p[-1])
    pilaTipos.append(tipo)
    direccion = directorio.directorio[funcionActual][1].regresarDireccion(
        p[-1])
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
        op_izq = pilaOper.pop()
        dir_der = pilaDir.pop()
        tipo_izq = Semantica.obtener_tipo(pilaTipos.pop())
        operador = pOper.pop()
        tipo_resultado = Semantica.tipo_resultado(operador, tipo_izq, tipo_der)
        dir_izq = pilaDir.pop()

        if tipo_resultado != -1:
            global contadorAvail
            global direccionAvail
            global contadorCuadruplos
            contadorCuadruplos += 1
            resultado = "t" + str(contadorAvail)
            pilaDir.append(direccionAvail + contadorAvail)
            contadorAvail = contadorAvail + 1
            pilaCuadruplos.append([operador, op_der, op_izq, resultado])
            pilaOper.append(resultado)
            pilaTipos.append(Semantica.obtener_token(tipo_resultado))
            pCuadruplos.generarCuadruplo(
                contadorCuadruplos, operador, dir_izq, dir_der, pilaDir[-1])
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
        op_izq = pilaOper.pop()
        dir_der = pilaDir.pop()
        tipo_izq = Semantica.obtener_tipo(pilaTipos.pop())
        operador = pOper.pop()
        tipo_resultado = Semantica.tipo_resultado(operador, tipo_izq, tipo_der)
        dir_izq = pilaDir.pop()

        if tipo_resultado != -1:
            global contadorAvail
            global direccionAvail
            global contadorCuadruplos
            contadorCuadruplos += 1
            resultado = "t" + str(contadorAvail)
            pilaDir.append(direccionAvail + contadorAvail)
            contadorAvail = contadorAvail + 1
            pilaCuadruplos.append([operador, op_der, op_izq, resultado])
            pilaOper.append(resultado)
            pilaTipos.append(Semantica.obtener_token(tipo_resultado))
            pCuadruplos.generarCuadruplo(
                contadorCuadruplos, operador, dir_izq, dir_der, pilaDir[-1])
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
        op_izq = pilaOper.pop()
        dir_der = pilaDir.pop()
        tipo_izq = Semantica.obtener_tipo(pilaTipos.pop())
        operador = pOper.pop()
        tipo_resultado = Semantica.tipo_resultado(operador, tipo_izq, tipo_der)
        dir_izq = pilaDir.pop()

        if tipo_resultado != -1:
            global contadorAvail
            global direccionAvail
            global contadorCuadruplos
            contadorCuadruplos += 1
            resultado = "t" + str(contadorAvail)
            pilaDir.append(direccionAvail + contadorAvail)
            contadorAvail = contadorAvail + 1
            pilaCuadruplos.append([operador, op_der, op_izq, resultado])
            pilaOper.append(resultado)
            pilaTipos.append(Semantica.obtener_token(tipo_resultado))
            pCuadruplos.generarCuadruplo(
                contadorCuadruplos, operador, dir_izq, dir_der, pilaDir[-1])
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
        op_izq = pilaOper.pop()
        dir_der = pilaDir.pop()
        tipo_izq = Semantica.obtener_tipo(pilaTipos.pop())
        operador = pOper.pop()
        tipo_resultado = Semantica.tipo_resultado(operador, tipo_izq, tipo_der)
        dir_izq = pilaDir.pop()

        if tipo_resultado != -1:
            global contadorAvail
            global direccionAvail
            global contadorCuadruplos
            contadorCuadruplos += 1
            resultado = "t" + str(contadorAvail)
            pilaDir.append(direccionAvail + contadorAvail)
            contadorAvail = contadorAvail + 1
            pilaCuadruplos.append([operador, op_der, op_izq, resultado])
            pilaOper.append(resultado)
            pilaTipos.append(Semantica.obtener_token(tipo_resultado))
            pCuadruplos.generarCuadruplo(
                contadorCuadruplos, operador, dir_izq, dir_der, pilaDir[-1])
            print(f"Se genero cuadruplo {pilaCuadruplos[-1]}")
        else:
            print("Error - Tipo de dato erroneo")
            quit()

# FONDOS FALSOS


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


# FUNCIONES

def p_bloque_funciones(p):
    '''bloque_funciones : FUNCS DOSPUNTOS definicion_funciones'''


def p_definicion_funciones(p):
    '''definicion_funciones : tipo_funcion id_funcion PARIZQ funcion_params PARDER DOSPUNTOS bloque_funcion_variables funcion_bloque_codigo regresa_bloque definicion_funcion'''


def p_definicion_funcion(p):
    '''definicion_funcion : definicion_funciones 
        | empty'''


def p_tipo_funcion(p):
    '''tipo_funcion : ENTERO
                    | FLOTANTE
                    | TEXTO
                    | LOGICO'''

    global tipoFuncion
    tipoFuncion = p[1]


def p_id_funcion(p):
    '''id_funcion : ID'''
    global idFuncion
    global funcionActual
    idFuncion = p[1]
    funcionActual = idFuncion
    directorio.agregarNuevaFuncion(idFuncion, tipoFuncion)
    directorio.asignarTablaVariablesLocales(idFuncion)
    directorio.crearArregloTiposParam(idFuncion)


def p_funcion_params(p):
    '''funcion_params : tipo_param_funcion id_param_funcion funcion_param
    | empty'''


def p_tipo_param_funcion(p):
    '''tipo_param_funcion : ENTERO
                    | FLOTANTE
                    | TEXTO
                    | LOGICO'''

    global tipoParamFuncion
    tipoParamFuncion = p[1]


def p_id_param_funcion(p):
    '''id_param_funcion : ID'''
    global idParamFuncion
    idParamFuncion = p[1]
    p_pn_agrega_variable_local_param(idParamFuncion)
    directorio.agregarTipoParametrosFuncion(idFuncion, tipoParamFuncion)


def p_funcion_param(p):
    '''funcion_param : COMA funcion_params 
        | empty'''


def p_bloque_funcion_variables(p):
    '''bloque_funcion_variables : VARS DOSPUNTOS funcion_bloque_variables'''


def p_funcion_bloque_variables(p):
    '''funcion_bloque_variables : funcion_variables 
    | empty '''


def p_funcion_variables(p):
    '''funcion_variables : VAR funcion_tipo_variable funcion_id_variables PUNTOCOMA funcion_variable_2'''


def p_funcion_variable_2(p):
    '''funcion_variable_2 : funcion_variables
                | empty'''


def p_funcion_tipo_variable(p):
    '''funcion_tipo_variable : ENTERO
                    | FLOTANTE
                    | TEXTO
                    | LOGICO'''

    global tipoVariableFuncion
    tipoVariableFuncion = p[1]


def p_funcion_id_variables(p):
    '''funcion_id_variables : id_variable_local_funcion funcion_id_variable
        | empty'''


def p_id_variable_local_funcion(p):
    '''id_variable_local_funcion : ID'''
    p_pn_agrega_variable_local(p)


def p_funcion_id_variable(p):
    '''funcion_id_variable : COMA funcion_id_variables
                    | empty'''


def p_funcion_bloque_codigo(p):
    '''funcion_bloque_codigo : BLOQUE DOSPUNTOS bloque'''


def p_regresa_bloque(p):
    '''regresa_bloque : REGRESA'''
    # REGRESAR LOS ESPACIOS DE MEMORIA A CERO
    directorio.directorio[idFuncion][1].imprimirTablaVariables()
    directorio.limpiarTablaVariablesLocales(idFuncion)
    global funcionActual
    global cle, clf, cll, clt
    funcionActual = nombrePrograma
    cle = 0
    clf = 0
    clt = 0
    cll = 0


# Ejecutar Codigo
code = open("prueba", 'r')
data = str(code.read())
yacc.yacc()
yacc.parse(data)
lexer = lexico.lexer
lexer.input(data)
# for tok in lexer:
# print(tok)
