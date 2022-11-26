import ply.yacc as yacc
import lexico
from directorio import Directorio
from semantica import Semantica
from cuadruplos import Cuadruplos
from directorio import Constantes
from maquinaVirtual import MaquinaVirtual
tokens = lexico.tokens

pilaTipos = []
pilaOper = []
pilaDir = []
pOper = [""]
pilaCuadruplos = []
pilaSaltos = []
contadorAvail = 0
direccionAvail = 200000
pCuadruplos = Cuadruplos()
contadorCuadruplos = 0
parameterCounterK = 0

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


# ----- GRAMATICA Y PNS DE ESTRUCTURA DEL PROGRAMA -----
def p_inicio(p):
    '''inicio : LPESP ID pn_crear_directorio PUNTOCOMA pn_generaroGOTOMAIN VARS DOSPUNTOS pn_crear_tabla_variables bloque_variables bloque_funciones ESP DOSPUNTOS pn_rellenaGOTOMAIN bloque PSE PUNTOCOMA pn_terminar_programa'''


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


def p_pn_crear_tabla_variables(p):
    '''pn_crear_tabla_variables : empty'''
    directorio.crearTablaVariables(nombrePrograma)


def p_pn_generaroGOTOMAIN(p):
    '''pn_generaroGOTOMAIN : empty'''
    global contadorCuadruplos
    contadorCuadruplos += 1
    pCuadruplos.generarCuadruplo(
        contadorCuadruplos, "GOTO MAIN", "", "", "PENDIENTE")
    pilaSaltos.append(contadorCuadruplos)
    print("GOTOMAIN", pilaSaltos)


def p_pn_rellenaGOTOMAIN(p):
    '''pn_rellenaGOTOMAIN : empty'''
    print(pilaSaltos)
    global contadorCuadruplos
    uno = pilaSaltos.pop()
    pCuadruplos.rellenarSalto(uno, contadorCuadruplos + 1)


def p_pn_terminar_programa(p):
    '''pn_terminar_programa : empty'''
    # directorio.eliminarTablaVariables(nombrePrograma)
    # directorio.eliminarFuncion(nombrePrograma)
    # print(f"\n Cuadruplos Generados \n")
    f = open("archivoOBJ", "w")

    directorio.imprimirTabla()
    tablaConstantes.imprimir()
    pCuadruplos.imprimir()
    f.close()


def p_bloque_variables(p):
    '''bloque_variables : matrices bloque_variables
                        | arreglos bloque_variables
                        | variables bloque_variables
                        | empty '''
# # ----- GRAMATICA Y PNS DE DECLARACION DE VARIABLES -----


def p_variables(p):
    '''variables : VAR tipo_variable id_variable PUNTOCOMA variables
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
    directorio.directorio[funcionActual][1].crear(
        p[-1], tipoVariable, direccion)
    print("VARIABLES GLOBALES", cge, cgf, cgt, cgl)


# ----- GRAMATICA Y PNS DE DECLARACION DE ARREGLOS -----
def p_arreglos(p):
    '''arreglos : ARREGLO tipo_variable ID pn_agrega_variable_arreglo CORIZQ CTEENT pn_agregar_dimension CORDER PUNTOCOMA
                | empty'''


def p_pn_agrega_variable_arreglo(p):
    '''pn_agrega_variable_arreglo : empty'''
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

    global id_arreglo
    id_arreglo = p[-1]
    directorio.directorio[funcionActual][1].crear(
        id_arreglo, tipoVariable, direccion, True)


def p_pn_agregar_dimension(p):
    '''pn_agregar_dimension : empty'''
    dimension = p[-1]
    global cge, cgf, cgl, cgt
    if tipoVariable == "entero":
        cge += dimension
    elif tipoVariable == "flotante":
        cgf += dimension
    elif tipoVariable == "texto":
        cgt += dimension
    elif tipoVariable == "logico":
        cgl += dimension
    directorio.directorio[funcionActual][1].agregarTraslado(
        id_arreglo, dimension)

# ----- GRAMATICA Y PNS DE MATRICES -----


def p_matrices(p):
    '''matrices : MATRIZ tipo_variable ID pn_agrega_variable_arreglo CORIZQ CTEENT pn_guarda_dim1 CORDER CORIZQ CTEENT pn_guarda_dim2 CORDER PUNTOCOMA
                | empty'''


def p_pn_guarda_dim1(p):
    '''pn_guarda_dim1 : empty'''
    global dim1
    dim1 = p[-1]


def p_pn_guarda_dim2(p):
    '''pn_guarda_dim2 : empty'''
    dimension = dim1 * p[-1]

    global cge, cgf, cgl, cgt
    if tipoVariable == "entero":
        cge += dimension
    elif tipoVariable == "flotante":
        cgf += dimension
    elif tipoVariable == "texto":
        cgt += dimension
    elif tipoVariable == "logico":
        cgl += 1

    directorio.directorio[funcionActual][1].agregarTraslado(
        id_arreglo, dim1, p[-1], dimension)


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
    '''asigna : asignaID megaexpr pn_asignar PUNTOCOMA'''


def p_asginaID(p):
    '''asignaID : ID pn_agregar_id IGUAL pn_agregar_igual
                | ID pn_agregar_idarreglo CORIZQ exp pn_crear_cuadruplo_arreglo CORDER asigna_matriz'''


def p_asigna_matriz(p):
    '''asigna_matriz : CORIZQ exp pn_crear_cuadruplo_matriz CORDER IGUAL pn_agregar_igual
                    | IGUAL pn_agregar_igual'''


def p_pn_agregar_idarreglo(p):
    '''pn_agregar_idarreglo : empty'''
    global id_arreglo
    id_arreglo = p[-1]
    print(id_arreglo)
    pilaOper.append(p[-1])
    tipo = directorio.directorio[funcionActual][1].regresarTipo(p[-1])
    pilaTipos.append(tipo)


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
    dir_der = pilaDir.pop()
    dir_izq = pilaDir.pop()

    if tipo_izq == tipo_der or (tipo_izq == 'flotante' and tipo_der == 'entero'):
        global contadorAvail, contadorCuadruplos
        contadorCuadruplos += 1
        pilaCuadruplos.append([operador, op_der, "", op_izq])
        pCuadruplos.generarCuadruplo(
            contadorCuadruplos, operador, dir_der, "", dir_izq)
        print(f"Se genero cuadruplo {pilaCuadruplos[-1]}")
        print("TORO", contadorCuadruplos, dir_der, dir_izq)

    else:
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
    pCuadruplos.generarCuadruplo(
        contadorCuadruplos, "IMPRIME", "", "", pilaDir.pop())
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
    pCuadruplos.generarCuadruplo(
        contadorCuadruplos, "LEER", "", "", dir_variable)
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
    pCuadruplos.generarCuadruplo(
        contadorCuadruplos, "GOTOF", dir, "", "PENDIENTE")
    print(f"Se genero cuadruplo {pilaCuadruplos[-1]}")
    pilaSaltos.append(contadorCuadruplos)
    print(f"Pila SALTOS: {pilaSaltos}")


def p_pn_salida_if(p):
    '''pn_salida_if : empty'''
    print(f"\nPila SALTOS: {pilaSaltos}")
    pendiente = pilaSaltos.pop()
    pCuadruplos.rellenarSalto(pendiente, contadorCuadruplos + 1)
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
    pCuadruplos.rellenarSalto(falso, contadorCuadruplos+1)
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
    pCuadruplos.generarCuadruplo(
        contadorCuadruplos, "GOTOT", dir, "", retorno)
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
    pCuadruplos.generarCuadruplo(
        contadorCuadruplos, "GOTOF", dir, "", "PENDIENTE")
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

    pCuadruplos.rellenarSalto(falso, contadorCuadruplos+1)
    print(f"Pila SALTOS: {pilaSaltos}")


# ----- GRAMATICA DE EXPRESIONES -----
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
    '''var_cte : ID pn_agregar_id acceder_arreglo
            | ID pn_agregar_id llamada_funcion
            | CTEENT pn_agregar_ENT
            | CTEFLOT pn_agregar_FLOT
            | CTETEXTO pn_agregar_TEXTO
            | FALSO pn_agregar_LOGICO
            | VERDADERO pn_agregar_LOGICO
            | NULO pn_agregar_NULO'''


def p_acceder_arreglo(p):
    '''acceder_arreglo : CORIZQ pn_verificar_arreglo exp pn_crear_cuadruplo_arreglo CORDER acceder_matriz
                    | empty'''

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


def agrega_variable_local(p):
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
        p, tipoVariableFuncion, direccion)
    print("VARIABLES LOCALES", cle, clf, clt, cll)


def agrega_variable_local_param(p):
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
def p_acceder_matriz(p):
    '''acceder_matriz : CORIZQ pn_verificar_matriz exp pn_crear_cuadruplo_matriz CORDER
                    | empty'''

# ----- PNS DE EXPRESIONES -----

# AGREGAR ID


def p_pn_agregar_id(p):
    '''pn_agregar_id : empty'''
    # Si se busca en el main
    if funcionActual == nombrePrograma:
        directorio.directorio[nombrePrograma][1].verificarVariable(p[-1])
        pilaOper.append(p[-1])
        tipo = directorio.directorio[nombrePrograma][1].regresarTipo(p[-1])
        pilaTipos.append(tipo)
        direccion = directorio.directorio[nombrePrograma][1].regresarDireccion(
            p[-1])
        pilaDir.append(direccion)
    # Si se busca en una funcion
    else:
        # Es variable global
        if directorio.directorio[nombrePrograma][1].existeVariableLocal(p[-1]):
            pilaOper.append(p[-1])
            tipo = directorio.directorio[nombrePrograma][1].regresarTipo(p[-1])
            pilaTipos.append(tipo)
            direccion = directorio.directorio[nombrePrograma][1].regresarDireccion(
                p[-1])
            pilaDir.append(direccion)

        else:
            directorio.directorio[funcionActual][1].verificarVariable(p[-1])
            pilaOper.append(p[-1])
            tipo = directorio.directorio[funcionActual][1].regresarTipo(p[-1])
            pilaTipos.append(tipo)
            direccion = directorio.directorio[funcionActual][1].regresarDireccion(
                p[-1])
            pilaDir.append(direccion)

# AGREGAR CONSTANTES


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
        pilaOper.append("FALSO")
    else:
        pilaDir.append(tablaConstantes.regresarDireccion("VERDADERO"))
        pilaOper.append("VERDADERO")
    pilaTipos.append("logico")


def p_pn_agregar_NULO(p):
    '''pn_agregar_NULO : empty'''
    global ccl
    global constantes
    pilaDir.append(tablaConstantes.regresarDireccion("NULO"))
    pilaOper.append(p[-1])
    pilaTipos.append("nulo")

# ----- PNS DE ACCEDER ARREGLOS -----


def p_pn_verificar_arreglo(p):
    '''pn_verificar_arreglo : empty'''
    global id_arreglo
    id_arreglo = pilaOper[-1]
    directorio.directorio[funcionActual][1].verificarArreglo(id_arreglo)


def p_pn_crear_cuadruplo_arreglo(p):
    '''pn_crear_cuadruplo_arreglo : empty'''
    print(f"Tipos: {pilaTipos}")
    print(f"Operandos: {pilaOper}")
    print(f"Operadores: {pOper}")
    print(f"Direccion : {pilaDir}")
    if directorio.directorio[funcionActual][1].esArregloMatriz(id_arreglo) == 5:
        return
    global contadorCuadruplos
    contadorCuadruplos += 1
    indice = pilaOper.pop()
    tipos = pilaTipos.pop()
    dir_indice = pilaDir.pop()
    if tipos != "entero":
        print("Error - Indice debe ser entero")
        quit()

    dimension = directorio.directorio[funcionActual][1].regresaDimension(
        id_arreglo)
    pCuadruplos.generarCuadruplo(
        contadorCuadruplos, "VERIFICADIM", dir_indice, 0, dimension)

    base = pilaOper.pop()
    dir_base = directorio.directorio[funcionActual][1].regresarDireccion(
        id_arreglo)

    global contadorAvail
    global direccionAvail

    contadorCuadruplos += 1

    pilaDir.append(f"({direccionAvail + contadorAvail})")
    contadorAvail = contadorAvail + 1

    pCuadruplos.generarCuadruplo(
        contadorCuadruplos, "+DIR", dir_indice, dir_base, direccionAvail + + contadorAvail - 1)
    pilaOper.append(f"({pilaDir[-1]})")


def p_pn_verificar_matriz(p):
    '''pn_verificar_matriz : empty'''
    directorio.directorio[funcionActual][1].verificarMatriz(id_arreglo)


def p_pn_crear_cuadruplo_matriz(p):
    '''pn_crear_cuadruplo_matriz : empty'''
    if directorio.directorio[funcionActual][1].esArregloMatriz(id_arreglo) != 5:
        print(
            f"Error - Se esta tratando de acceder a {id_arreglo} como matriz")
        quit()
    print(f"Tipos: {pilaTipos}")
    print(f"Operandos: {pilaOper}")
    print(f"Operadores: {pOper}")
    print(f"Direccion : {pilaDir}")
    global contadorCuadruplos

    j = pilaOper.pop()
    tipo = pilaTipos.pop()
    dir_j = pilaDir.pop()
    if tipo != "entero":
        print("Error - Indice debe ser entero")
        quit()

    i = pilaOper.pop()
    tipo = pilaTipos.pop()
    dir_i = pilaDir.pop()
    if tipo != "entero":
        print("Error - Indice debe ser entero")
        quit()

    d1, d2 = directorio.directorio[funcionActual][1].regresaDimensionM(
        id_arreglo)
    dir_d1 = tablaConstantes.regresarDireccion(d1)
    dir_d2 = tablaConstantes.regresarDireccion(d2)
    contadorCuadruplos += 1
    pCuadruplos.generarCuadruplo(
        contadorCuadruplos, "VERIFICADIM", dir_i, 0, d1)
    contadorCuadruplos += 1
    pCuadruplos.generarCuadruplo(
        contadorCuadruplos, "VERIFICADIM", dir_j, 0, d2)

    base = pilaOper.pop()
    dir_base = directorio.directorio[funcionActual][1].regresarDireccion(
        id_arreglo)

    global contadorAvail
    global direccionAvail

    t0 = direccionAvail + contadorAvail
    contadorAvail = contadorAvail + 1

    t1 = direccionAvail + contadorAvail
    contadorAvail = contadorAvail + 1
    pilaDir.append(f"({direccionAvail + contadorAvail})")
    contadorAvail = contadorAvail + 1
    apuntador = pilaDir[-1]

    contadorCuadruplos += 1
    pCuadruplos.generarCuadruplo(contadorCuadruplos, "*", dir_i, dir_d2, t0)
    contadorCuadruplos += 1
    pCuadruplos.generarCuadruplo(contadorCuadruplos, "+", t0, dir_j, t1)
    contadorCuadruplos += 1
    pCuadruplos.generarCuadruplo(
        contadorCuadruplos, "+DIR", t1, dir_base, direccionAvail + contadorAvail - 1)
    if dir_base in pilaDir:
        pilaDir.remove(dir_base)

    pilaOper.append(f"({pilaDir[-1]})")
    print(f"Tipos: {pilaTipos}")
    print(f"Operandos: {pilaOper}")
    print(f"Operadores: {pOper}")
    print(f"Direccion : {pilaDir}")
    print("\n")


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
            pilaCuadruplos.append([operador, op_izq, op_der, resultado])
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
            pilaCuadruplos.append([operador, op_izq, op_der, resultado])
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
            pilaCuadruplos.append([operador, op_izq, op_der, resultado])
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
            pilaCuadruplos.append([operador, op_izq, op_der, resultado])
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


# ----- GRAMATICAS EXTRA -----
def p_error(p):
    print(f"Error de sintaxis en {p}")
    exit()


def p_empty(p):
    '''empty : '''
    pass


# Definicion Funciones

def p_bloque_funciones(p):
    '''bloque_funciones : FUNCS DOSPUNTOS definicion_funciones'''


def p_definicion_funciones(p):
    '''definicion_funciones : tipo_funcion ID pn_agrega_variable pn_insertar_funcion_tabla PARIZQ funcion_params PARDER DOSPUNTOS bloque_funcion_variables bloque_funcion_codigo regresa_bloque definicion_funcion
                        | empty'''


def p_definicion_funcion(p):
    '''definicion_funcion : definicion_funciones
        | empty'''


def p_tipo_funcion(p):
    '''tipo_funcion : ENTERO
                    | FLOTANTE
                    | TEXTO
                    | LOGICO
                    | NULO'''

    global tipoFuncion
    global tipoVariable
    tipoFuncion = p[1]
    tipoVariable = tipoFuncion


def p_pn_insertar_funcion_tabla(p):
    '''pn_insertar_funcion_tabla : empty'''
    global idFuncion
    global funcionActual
    idFuncion = p[-2]
    funcionActual = idFuncion
    directorio.agregarNuevaFuncion(idFuncion, tipoFuncion)
    directorio.crearTablaVariables(idFuncion)


def p_funcion_params(p):
    '''funcion_params : tipo_param_funcion ID pn_agregar_parametro_funcion funcion_param
    | empty'''


def p_tipo_param_funcion(p):
    '''tipo_param_funcion : ENTERO
                    | FLOTANTE
                    | TEXTO
                    | LOGICO'''

    global tipoParamFuncion
    tipoParamFuncion = p[1]


def p_pn_agregar_parametro_funcion(p):
    '''pn_agregar_parametro_funcion : empty'''
    global idParamFuncion
    idParamFuncion = p[-1]
    agrega_variable_local_param(idParamFuncion)
    directorio.agregarTipoParametrosFuncion(idFuncion, tipoParamFuncion)


def p_funcion_param(p):
    '''funcion_param : COMA funcion_params
        | empty'''


def p_bloque_funcion_variables(p):
    '''bloque_funcion_variables : VARS DOSPUNTOS funcion_bloque_variables pn_guardar_cuadruplo_inicio_funcion'''


def p_pn_guardar_cuadruplo_inicio_funcion(p):
    '''pn_guardar_cuadruplo_inicio_funcion : empty'''
    directorio.guardarContadorCuadruplos(idFuncion, contadorCuadruplos+1)


def p_funcion_bloque_variables(p):
    '''funcion_bloque_variables : funcion_variables
    | empty '''


def p_funcion_variables(p):
    '''funcion_variables : VAR funcion_tipo_variable funcion_id_variables PUNTOCOMA funcion_variable'''


def p_funcion_variable(p):
    '''funcion_variable : funcion_variables
                | empty'''


def p_funcion_tipo_variable(p):
    '''funcion_tipo_variable : ENTERO
                    | FLOTANTE
                    | TEXTO
                    | LOGICO'''

    global tipoVariableFuncion
    tipoVariableFuncion = p[1]


def p_funcion_id_variables(p):
    '''funcion_id_variables : ID pn_agrega_variable_local funcion_id_variable
        | empty'''


def p_pn_agrega_variable_local(p):
    '''pn_agrega_variable_local : empty'''
    agrega_variable_local(p[-1])
    directorio.contadorNuevaVariableLocal(idFuncion)


def p_funcion_id_variable(p):
    '''funcion_id_variable : COMA funcion_id_variables
                    | empty'''


def p_bloque_funcion_codigo(p):
    '''bloque_funcion_codigo : BLOQUE DOSPUNTOS bloque'''


def p_regresa_bloque(p):
    '''regresa_bloque : REGRESA expr pn_verificar_tipo_retorno PUNTOCOMA'''


def p_pn_verificar_tipo_retorno(p):
    '''pn_verificar_tipo_retorno : empty'''
    global argumento
    global tipoArgumento
    global funcionActual
    global cle, clf, cll, clt
    argumento = pilaOper.pop()
    tipoArgumento = pilaTipos.pop()
    memoria = pilaDir.pop()
    if tipoArgumento != directorio.directorio[idFuncion][0]:
        print(
            f"El valor de retorno de la funcion {idFuncion} de tipo {tipoArgumento} no coincide con el esperado.")
        exit()
    else:
        # REGRESAR LOS ESPACIOS DE MEMORIA A CERO
        directorio.directorio[idFuncion][1].imprimirTablaVariables()
        funcionActual = nombrePrograma
        cle = 0
        clf = 0
        clt = 0
        cll = 0
        global contadorCuadruplos
        contadorCuadruplos += 1
        pilaCuadruplos.append(["RET", "", "", memoria])
        pCuadruplos.generarCuadruplo(
            contadorCuadruplos, "RET", "", "", memoria)
        contadorCuadruplos += 1
        pilaCuadruplos.append(["ENDFunc", "", "", ""])
        pCuadruplos.generarCuadruplo(
            contadorCuadruplos, "ENDFunc", "", "", "")


# Llamada Funciones
def p_llamada_funcion(p):
    '''llamada_funcion : PARIZQ pn_verificar_funcion_existe bloque_expresiones_llamada_funciones_padre PARDER pn_verificar_numero_de_parametros'''


def p_pn_verificar_funcion_existe(p):
    '''pn_verificar_funcion_existe : empty'''
    global id_funcion_a_checar
    id_funcion_a_checar = pilaOper[-1]
    directorio.verificarFuncionExiste(id_funcion_a_checar)
    global contadorCuadruplos
    contadorCuadruplos += 1
    pilaCuadruplos.append(["ERA", "", "", id_funcion_a_checar])
    pCuadruplos.generarCuadruplo(
        contadorCuadruplos, "ERA", "", "", id_funcion_a_checar)


def p_bloque_expresiones_llamada_funciones_padre(p):
    '''bloque_expresiones_llamada_funciones_padre : bloque_expresiones_llamada_funciones
    | empty'''


def p_bloque_expresiones_llamada_funciones(p):
    '''bloque_expresiones_llamada_funciones : megaexpr pn_verificar_tipo_parametro bloque_expresiones_llamada_funcion'''


def p_bloque_expresiones_llamada_funcion(p):
    '''bloque_expresiones_llamada_funcion : COMA bloque_expresiones_llamada_funciones
    | empty'''


def p_pn_verificar_tipo_parametro(p):
    '''pn_verificar_tipo_parametro : empty'''
    global argumento
    global tipoArgumento
    global parameterCounterK
    global memoriaExp
    memoriaExp = pilaDir.pop()
    parameterCounterK += 1
    argumento = pilaOper.pop()
    tipoArgumento = pilaTipos.pop()
    if directorio.directorio[id_funcion_a_checar][3] >= parameterCounterK and tipoArgumento != directorio.directorio[id_funcion_a_checar][2][parameterCounterK-1]:
        print(
            f"El parametro {parameterCounterK} de la funcion {id_funcion_a_checar} de tipo {tipoArgumento} no coincide con el esperado.")
        exit()
    else:
        global contadorCuadruplos
        contadorCuadruplos += 1
        argumentok = "param" + str(parameterCounterK+1)
        pilaCuadruplos.append(
            ["PARAMETER", argumento, "", argumentok])
        global cle, clf, cll, clt
        if tipoArgumento == "entero":
            cle += 1
            direccion = 10000 + cle
        elif tipoArgumento == "flotante":
            clf += 1
            direccion = 50000 + clf
        elif tipoArgumento == "texto":
            clt += 1
            direccion = 90000 + clt
        elif tipoArgumento == "logico":
            cll += 1
            direccion = 130000 + cll

        pCuadruplos.generarCuadruplo(
            contadorCuadruplos, "PARAMETER", memoriaExp, "", direccion)


def p_pn_verificar_numero_de_parametros(p):
    '''pn_verificar_numero_de_parametros : empty'''
    global parameterCounterK
    if directorio.directorio[id_funcion_a_checar][3] != parameterCounterK:
        print(
            f"La llamada de la funcion {id_funcion_a_checar} contiene un numero incorrecto de parametros.")
        exit()
    else:
        global contadorCuadruplos
        contadorCuadruplos += 1
        parameterCounterK = 0
        pilaCuadruplos.append(
            ["GOSUB", id_funcion_a_checar, "", directorio.directorio[id_funcion_a_checar][5]])
        pCuadruplos.generarCuadruplo(
            contadorCuadruplos, "GOSUB", id_funcion_a_checar, "", directorio.directorio[id_funcion_a_checar][5])

        direccionGlobalFuncion = directorio.directorio[nombrePrograma][1].regresarDireccion(
            id_funcion_a_checar)
        tipoFuncion = directorio.directorio[id_funcion_a_checar][0]

        global contadorAvail
        global direccionAvail
        contadorCuadruplos += 1
        resultado = "t" + str(contadorAvail)
        pilaDir.pop()
        pilaOper.pop()
        pilaTipos.pop()

        pilaDir.append(direccionAvail + contadorAvail)
        pilaOper.append(resultado)
        pilaTipos.append(tipoFuncion)
        pilaCuadruplos.append(["=", direccionGlobalFuncion, "", resultado])
        pCuadruplos.generarCuadruplo(
            contadorCuadruplos, "=", direccionGlobalFuncion, "", direccionAvail + contadorAvail)
        contadorAvail = contadorAvail + 1


"""
print(directorio.directorio[nombrePrograma])
        pilaCuadruplos.append(
            ["=", "", "", direccion])
        pCuadruplos.generarCuadruplo(
            contadorCuadruplos, "=", "", "", direccion)
"""


# ----- EJECUTAR CODIGO -----
print("Bienvenido a LPESP")
archivo = input("Escribe el nombre del archivo a leer:")
code = open(archivo, 'r')
data = str(code.read())
yacc.yacc()
yacc.parse(data)
lexer = lexico.lexer
lexer.input(data)
mv = MaquinaVirtual(nombrePrograma, pCuadruplos,
                    directorio, tablaConstantes)
mv.ejecucion()
# for tok in lexer:
# print(tok)
