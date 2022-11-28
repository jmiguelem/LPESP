from directorio import Directorio
from directorio import Constantes
from directorio import TablaVariables
from memoriaVirtual import MemoriaVirtual


class MaquinaVirtual:
    cuadruplos = []
    nombrePrograma = ""
    migajas = []
    valorReturn = ""
    codigosOperaciones = {
        'GOTO MAIN': 0,
        '=': 1,
        '+': 2,
        '-': 3,
        '*': 4,
        '/': 5,
        'ENDFunc': 6,
        'ERA': 7,
        'PARAMETER': 8,
        'GOSUB': 9,
        'IMPRIME': 10,
        'LEER': 11,
        'GOTOF': 12,
        'GOTO': 13,
        'GOTOT': 14,
        'VERIFICADIM': 15,
        '+DIR': 16,
        '<': 17,
        '>': 18,
        '<>': 19,
        '==': 20,
        '||': 21,
        '&&': 22,
        'RET': 23
    }
    directorioFunciones = Directorio()
    tablaConstantes = Constantes()
    memoriaGlobal = MemoriaVirtual()
    memoriaConstantes = MemoriaVirtual()
    memoriaTemporales = MemoriaVirtual()
    memoriasLocales = []
    temporalMemoriaLocal = MemoriaVirtual()

    def __init__(self, nombrePrograma, cuadruplos, directorio, tablaConstantes):
        self.nombrePrograma = nombrePrograma
        self.cuadruplos = cuadruplos
        self.directorioFunciones = directorio
        self.tablaConstantes = tablaConstantes
        self.inicializarCuadruplos()
        self.inicializarMemoriaVirtual()

    def inicializarCuadruplos(self):
        pila = self.cuadruplos.pilaCuadruplos
        for indice in pila:
            cuadruplo = pila[indice]
            if cuadruplo[0] in self.codigosOperaciones:
                self.cuadruplos.pilaCuadruplos[indice][0] = self.codigosOperaciones[cuadruplo[0]]

    def obtenerValor(self, dirMemoria):
        # Memoria Global
        if dirMemoria >= 1000 and dirMemoria < 20000:
            return self.memoriaGlobal.obtenerValor(dirMemoria)
        # Memoria Local
        elif dirMemoria >= 20000 and dirMemoria < 39999:
            memoriaLocal = self.memoriasLocales[-1]
            return memoriaLocal.obtenerValor(dirMemoria)
        # Memoria Constante
        elif dirMemoria >= 40000 and dirMemoria < 49999:
            return self.memoriaConstantes.obtenerValor(dirMemoria)
        # Memoria Temporales
        elif dirMemoria >= 50000:
            return self.memoriaTemporales.obtenerValor(dirMemoria)

    def obtener_direccion(self, dirMemoria):
        # Memoria Global
        if dirMemoria >= 1000 and dirMemoria < 20000:
            return self.memoriaGlobal.obtenerDireccion(dirMemoria)
        # Memoria Local
        elif dirMemoria >= 20000 and dirMemoria < 39999:
            memoriaLocal = self.memoriasLocales[-1]
            return memoriaLocal.obtenerDireccion(dirMemoria)
        # Memoria Constante
        elif dirMemoria >= 40000 and dirMemoria < 49999:
            return self.memoriaConstantes.obtenerDireccion(dirMemoria)
        # Memoria Temporales
        elif dirMemoria >= 50000:
            return self.memoriaTemporales.obtenerDireccion(dirMemoria)

    def agregar(self, dirMemoria, id, valor):
        # Memoria Global
        if dirMemoria >= 1000 and dirMemoria < 20000:
            return self.memoriaGlobal.agregar(dirMemoria, id, valor)
        # Memoria Local
        elif dirMemoria >= 20000 and dirMemoria < 39999:
            memoriaLocal = self.memoriasLocales[-1]
            memoriaLocal.agregar(dirMemoria, id, valor)
        # Memoria Constante
        elif dirMemoria >= 40000 and dirMemoria < 49999:
            return self.memoriaConstantes.agregar(dirMemoria, id, valor)
        # Memoria Temporales
        elif dirMemoria >= 50000:
            return self.memoriaTemporales.agregar(dirMemoria, id, valor)

    def agregarArre(self, dirMemoria, id, valor, dimension1=None):
        # Memoria Global
        if dirMemoria >= 1000 and dirMemoria < 20000:
            return self.memoriaGlobal.agregarArre(dirMemoria, id, valor, dimension1)
        # Memoria Local
        elif dirMemoria >= 20000 and dirMemoria < 39999:
            memoriaLocal = self.memoriasLocales[-1]
            return memoriaLocal.agregarArre(dirMemoria, id, valor, dimension1)
        # Memoria Constante
        elif dirMemoria >= 40000 and dirMemoria < 49999:
            return self.memoriaConstantes.agregarArre(dirMemoria, id, valor, dimension1)
        # Memoria Temporales
        elif dirMemoria >= 50000:
            return self.memoriaTemporales.agregarArre(dirMemoria, id, valor, dimension1)

    def agregarMat(self, dirMemoria, id, valor, dimension1=None, dimension2=None, desplazo=None):
        # Memoria Global
        if dirMemoria >= 1000 and dirMemoria < 20000:
            self.memoriaGlobal.agregarMat(
                dirMemoria, id, valor, dimension1, dimension2, desplazo)
        # Memoria Local
        elif dirMemoria >= 20000 and dirMemoria < 39999:
            memoriaLocal = self.memoriasLocales[-1]
            memoriaLocal.agregarMat(
                dirMemoria, id, valor, dimension1, dimension2, desplazo)
        # Memoria Constante
        elif dirMemoria >= 40000 and dirMemoria < 49999:
            self.memoriaConstantes.agregarMat(
                dirMemoria, id, valor, dimension1, dimension2, desplazo)
        # Memoria Temporales
        elif dirMemoria >= 50000:
            self.memoriaTemporales.agregarMat(
                dirMemoria, id, valor, dimension1, dimension2, desplazo)

    def actualizarValor(self, dirMemoria, valor):  # Memoria Global
        if dirMemoria >= 1000 and dirMemoria < 20000:
            self.memoriaGlobal.actualizarValor(dirMemoria, valor)
        # Memoria Local
        elif dirMemoria >= 20000 and dirMemoria < 39999:
            memoriaLocal = self.memoriasLocales[-1]
            memoriaLocal.actualizarValor(dirMemoria, valor)
        # Memoria Constante
        elif dirMemoria >= 40000 and dirMemoria < 49999:
            self.memoriaConstantes.actualizarValor(dirMemoria, valor)
        # Memoria Temporales
        elif dirMemoria >= 50000:
            self.memoriaTemporales.actualizarValor(dirMemoria, valor)

    def actualizarId(self, dirMemoria, id):
        if dirMemoria >= 1000 and dirMemoria < 20000:
            return self.memoriaGlobal.actualizarId(dirMemoria, id)
        # Memoria Local
        elif dirMemoria >= 20000 and dirMemoria < 39999:
            memoriaLocal = self.memoriasLocales[-1]
            return memoriaLocal.actualizarId(dirMemoria, id)
        # Memoria Constante
        elif dirMemoria >= 40000 and dirMemoria < 49999:
            return self.memoriaConstantes.actualizarId(dirMemoria, id)
        # Memoria Temporales
        elif dirMemoria >= 50000:
            return self.memoriaTemporales.actualizarId(dirMemoria, id)

    def obtenerLen(self, dirMemoria):
        if dirMemoria >= 1000 and dirMemoria < 20000:
            return self.memoriaGlobal.obtenerLen(dirMemoria)
        # Memoria Local
        elif dirMemoria >= 20000 and dirMemoria < 39999:
            memoriaLocal = self.memoriasLocales[-1]
            return memoriaLocal.obtenerLen(dirMemoria)
        # Memoria Constante
        elif dirMemoria >= 40000 and dirMemoria < 49999:
            return self.memoriaConstantes.obtenerLen(dirMemoria)
        # Memoria Temporales
        elif dirMemoria >= 50000:
            return self.memoriaTemporales.obtenerLen(dirMemoria)

    def obtenerDimArreglo(self, dirMemoria):
        if dirMemoria >= 1000 and dirMemoria < 20000:
            return self.memoriaGlobal.obtenerDimArreglo(dirMemoria)
        # Memoria Local
        elif dirMemoria >= 20000 and dirMemoria < 39999:
            memoriaLocal = self.memoriasLocales[-1]
            return memoriaLocal.obtenerDimArreglo(dirMemoria)
        # Memoria Constante
        elif dirMemoria >= 40000 and dirMemoria < 49999:
            return self.memoriaConstantes.obtenerDimArreglo(dirMemoria)
        # Memoria Temporales
        elif dirMemoria >= 50000:
            return self.memoriaTemporales.obtenerDimArreglo(dirMemoria)

    def obtenerDimMatriz(self, dirMemoria):
        if dirMemoria >= 1000 and dirMemoria < 20000:
            return self.memoriaGlobal.obtenerDimMatriz(dirMemoria)
        # Memoria Local
        elif dirMemoria >= 20000 and dirMemoria < 39999:
            memoriaLocal = self.memoriasLocales[-1]
            return memoriaLocal.obtenerDimMatriz(dirMemoria)
        # Memoria Constante
        elif dirMemoria >= 40000 and dirMemoria < 49999:
            return self.memoriaConstantes.obtenerDimMatriz(dirMemoria)
        # Memoria Temporales
        elif dirMemoria >= 50000:
            return self.memoriaTemporales.obtenerDimMatriz(dirMemoria)

    def obtenerDims(self, dirMemoria):
        if dirMemoria >= 1000 and dirMemoria < 20000:
            return self.memoriaGlobal.obtenerDims(dirMemoria)
        # Memoria Local
        elif dirMemoria >= 20000 and dirMemoria < 39999:
            memoriaLocal = self.memoriasLocales[-1]
            return memoriaLocal.obtenerDims(dirMemoria)
        # Memoria Constante
        elif dirMemoria >= 40000 and dirMemoria < 49999:
            return self.memoriaConstantes.obtenerDims(dirMemoria)
        # Memoria Temporales
        elif dirMemoria >= 50000:
            return self.memoriaTemporales.obtenerDims(dirMemoria)

    def obtenerId(self, dirMemoria):
        if dirMemoria >= 1000 and dirMemoria < 20000:
            return self.memoriaGlobal.obtenerId(dirMemoria)
        # Memoria Local
        elif dirMemoria >= 20000 and dirMemoria < 39999:
            memoriaLocal = self.memoriasLocales[-1]
            return memoriaLocal.obtenerId(dirMemoria)
        # Memoria Constante
        elif dirMemoria >= 40000 and dirMemoria < 49999:
            return self.memoriaConstantes.obtenerId(dirMemoria)
        # Memoria Temporales
        elif dirMemoria >= 50000:
            return self.memoriaTemporales.obtenerId(dirMemoria)

    def borrarMemoriaLocal(self):
        self.memoriasLocales.pop()

    def validarTipo(self, direccion):
        pass

    def debug(self, indice):
        print(f"Corriendo cuaduplo: {indice}")

    def crearMemoriaLocal(self, nombre_funcion):
        # Tabla Locales
        global tablaVariablesLocales
        tablaVariablesLocales = TablaVariables()
        tablaVariablesLocales = self.directorioFunciones.directorio[nombre_funcion][1]

        # numeroParams = self.directorioFunciones.directorio[nombre_funcion][3]
        # numeroVars = self.directorioFunciones.directorio[nombre_funcion][4]
        memoriaLocalNueva = MemoriaVirtual()

        for variableLocal in tablaVariablesLocales.tabla:
            if len(tablaVariablesLocales.tabla[variableLocal]) == 3:
                dir = tablaVariablesLocales.tabla[variableLocal][1]
                dim = tablaVariablesLocales.tabla[variableLocal][2]

                memoriaLocalNueva.agregarArre(
                    dir, variableLocal, "OBJETO DE ARREGLO", dim)

                for i in range(dim):
                    memoriaLocalNueva.agregar(
                        dir+i + 1, f"{variableLocal}{i}", "")

            elif len(tablaVariablesLocales.tabla[variableLocal]) == 5:
                dir = tablaVariablesLocales.tabla[variableLocal][1]
                dim = tablaVariablesLocales.tabla[variableLocal][4]

                memoriaLocalNueva.agregarMat(
                    dir, variableLocal, "OBJETO DE ARREGLO", tablaVariablesLocales.tabla[variableLocal][2], tablaVariablesLocales.tabla[variableLocal][3], dim)

                for i in range(dim):
                    memoriaLocalNueva.agregar(
                        dir+i+1, f"{variableLocal}{i}", "")

            else:
                memoriaLocalNueva.agregar(
                    tablaVariablesLocales.tabla[variableLocal][1], variableLocal, "")

        self.memoriasLocales.append(memoriaLocalNueva)

    def inicializarMemoriaVirtual(self):
        # Tabla Constantes
        for constante in self.tablaConstantes.tablaConstantes:
            self.memoriaConstantes.agregar(
                self.tablaConstantes.tablaConstantes[constante], constante, constante)

        # Tabla Globales
        global tablaVariablesGlobales
        tablaVariablesGlobales = TablaVariables()
        tablaVariablesGlobales = self.directorioFunciones.directorio[self.nombrePrograma][1]

        for variable in tablaVariablesGlobales.tabla:

            if len(tablaVariablesGlobales.tabla[variable]) == 3:
                dir = tablaVariablesGlobales.tabla[variable][1]
                dim = tablaVariablesGlobales.tabla[variable][2]

                self.agregarArre(
                    dir, variable, "OBJETO DE ARREGLO", dim)

                for i in range(dim):
                    self.agregar(
                        dir+i + 1, f"{variable}{i}", "")

            elif len(tablaVariablesGlobales.tabla[variable]) == 5:
                dir = tablaVariablesGlobales.tabla[variable][1]
                dim = tablaVariablesGlobales.tabla[variable][4]

                self.agregarMat(
                    dir, variable, "OBJETO DE MATRIZ", tablaVariablesGlobales.tabla[variable][2], tablaVariablesGlobales.tabla[variable][3], dim)

                for i in range(dim):
                    self.agregar(dir+i+1, f"{variable}{i}", "")

            else:
                self.agregar(
                    tablaVariablesGlobales.tabla[variable][1], variable, "")

    def ejecucion(self):
        pila = self.cuadruplos.pilaCuadruplos
        indice = 1
        while indice <= len(pila):
            cuadruplo = pila[indice]
            # print(cuadruplo)

            if cuadruplo[0] == 0:  # GOTOMAIN
                indice = cuadruplo[-1]

            elif cuadruplo[0] == 1:  # ASIGNACION
                direccion_op1 = self.obtener_direccion(cuadruplo[1])
                valor = self.obtenerValor(direccion_op1)

                direccion_op2 = self.obtener_direccion(cuadruplo[-1])

                if direccion_op2 >= 1000 and direccion_op2 < 5000:
                    try:
                        valor = int(valor)
                    except:
                        print(
                            f"Error de Ejecucion - se esta tratando de asignar un tipo de dato incorrecto a: {variable}")
                        quit()
                elif direccion_op2 >= 5000 and direccion_op2 < 9000:
                    try:
                        valor = float(valor)
                    except:
                        print(
                            f"Error de Ejecucion - se esta tratando de asignar un tipo de dato incorrecto a: {variable}")
                        quit()
                elif direccion_op2 >= 9000 and direccion_op2 < 13000:
                    try:
                        valor = str(valor)
                    except:
                        print(
                            f"Error de Ejecucion - se esta tratando de asignar un tipo de dato incorrecto a: {variable}")
                        quit()
                self.actualizarValor(direccion_op2, valor)
                indice += 1

            # SUMA
            elif cuadruplo[0] == 2:
                direccion_op1 = self.obtener_direccion(cuadruplo[1])
                direccion_op2 = self.obtener_direccion(cuadruplo[2])
                direccion_resultado = self.obtener_direccion(cuadruplo[-1])

                op1 = self.obtenerValor(direccion_op1)
                op2 = self.obtenerValor(direccion_op2)

                resultado = op1 + op2

                self.actualizarValor(direccion_resultado, resultado)
                indice += 1

            # RESTA
            elif cuadruplo[0] == 3:
                direccion_op1 = self.obtener_direccion(cuadruplo[1])
                direccion_op2 = self.obtener_direccion(cuadruplo[2])
                direccion_resultado = self.obtener_direccion(cuadruplo[-1])

                op1 = self.obtenerValor(direccion_op1)
                op2 = self.obtenerValor(direccion_op2)

                resultado = op1 - op2

                self.actualizarValor(direccion_resultado, resultado)
                indice += 1

                # MULTIPLICACION
            elif cuadruplo[0] == 4:
                direccion_op1 = self.obtener_direccion(cuadruplo[1])
                direccion_op2 = self.obtener_direccion(cuadruplo[2])
                direccion_resultado = self.obtener_direccion(cuadruplo[-1])

                op1 = self.obtenerValor(direccion_op1)
                op2 = self.obtenerValor(direccion_op2)

                resultado = op1 * op2

                self.actualizarValor(direccion_resultado, resultado)
                indice += 1

            # DIVISION
            elif cuadruplo[0] == 5:
                direccion_op1 = self.obtener_direccion(cuadruplo[1])
                direccion_op2 = self.obtener_direccion(cuadruplo[2])
                direccion_resultado = self.obtener_direccion(cuadruplo[-1])

                op1 = self.obtenerValor(direccion_op1)
                op2 = self.obtenerValor(direccion_op2)

                try:
                    resultado = op1 / op2
                except:
                    print(
                        "Error - Error al hacer la division. Verifica valor de operadores")

                self.actualizarValor(dir_resultado, resultado)
                indice += 1

            elif cuadruplo[0] == 6:  # ENDFUNC
                indice_temp = self.migajas.pop()
                cuadruplo = pila[indice_temp]
                self.actualizarValor(cuadruplo[1], self.valorReturn)
                self.borrarMemoriaLocal()
                indice = indice_temp

            elif cuadruplo[0] == 7:  # ERA
                # CARGAR MEMORIA LOCAL
                self.crearMemoriaLocal(cuadruplo[-1])
                self.temporalMemoriaLocal = self.memoriasLocales.pop()
                indice += 1

            elif cuadruplo[0] == 8:  # PARAMETER
                direccion = cuadruplo[1]
                valor = self.obtenerValor(direccion)
                if cuadruplo[-1] >= 20000 and cuadruplo[-1] < 25000:
                    try:
                        valor = int(valor)
                    except:
                        print(
                            f"Error de Ejecucion - se esta tratando de asignar un tipo de dato incorrecto a: {variable}")
                        quit()
                elif cuadruplo[-1] >= 25000 and cuadruplo[-1] < 29000:
                    try:
                        valor = float(valor)
                    except:
                        print(
                            f"Error de Ejecucion - se esta tratando de asignar un tipo de dato incorrecto a: {variable}")
                        quit()
                elif cuadruplo[-1] >= 29000 and cuadruplo[-1] < 33000:
                    try:
                        valor = str(valor)
                    except:
                        print(
                            f"Error de Ejecucion - se esta tratando de asignar un tipo de dato incorrecto a: {variable}")
                        quit()
                self.memoriasLocales.append(self.temporalMemoriaLocal)
                self.actualizarValor(cuadruplo[-1], valor)

                indice += 1

            elif cuadruplo[0] == 9:  # GOSUB
                self.migajas.append(indice + 1)
                indice = cuadruplo[-1]

            elif cuadruplo[0] == 10:  # IMPRIME
                direccion = cuadruplo[-1]
                leng = self.obtenerLen(direccion)
                if leng == 3:
                    dim = self.obtenerDimArreglo(direccion)
                    valor = '['
                    for i in range(dim):
                        valor += str(self.obtenerValor(direccion + i + 1)) + " "
                    valor = valor[: -1]
                    valor += "]"

                elif leng == 5:
                    dim1, dim2 = self.obtenerDims(direccion)
                    dim = self.obtenerDimMatriz(direccion)
                    valor = '[ \n'
                    i = 0
                    for j in range(dim1):
                        for k in range(dim2):
                            valor += str(self.obtenerValor(direccion + i + 1)) + " "
                            i += 1
                        valor += "\n"
                    valor += "]"
                else:
                    valor = self.obtenerValor(direccion)
                    print(valor)
                indice += 1

            # LEER
            elif cuadruplo[0] == 11:
                variable = self.obtenerId(cuadruplo[-1])
                valor = input(f"Ingresa el valor de {variable}: ")
                if cuadruplo[-1] >= 1000 and cuadruplo[-1] < 5000:
                    try:
                        valor = int(valor)
                    except:
                        print(
                            f"Error de Ejecucion - se esta tratando de asignar un tipo de dato incorrecto a: {variable}")
                        quit()
                elif cuadruplo[-1] >= 5000 and cuadruplo[-1] < 9000:
                    try:
                        valor = float(valor)
                    except:
                        print(
                            f"Error de Ejecucion - se esta tratando de asignar un tipo de dato incorrecto a: {variable}")
                        quit()
                elif cuadruplo[-1] >= 9000 and cuadruplo[-1] < 13000:
                    try:
                        valor = str(valor)
                    except:
                        print(
                            f"Error de Ejecucion - se esta tratando de asignar un tipo de dato incorrecto a: {variable}")
                        quit()
                self.actualizarValor(cuadruplo[-1], valor)
                indice += 1

            # GOTOF
            elif cuadruplo[0] == 12:
                direccion = self.obtener_direccion(cuadruplo[1])
                if self.obtenerValor(direccion) == self.obtenerValor(46000) or self.obtenerValor(direccion) == False:
                    indice = cuadruplo[-1]
                else:
                    indice += 1

            # GOTO
            elif cuadruplo[0] == 13:
                indice = cuadruplo[-1]

            # GOTOT
            elif cuadruplo[0] == 14:
                direccion = self.obtener_direccion(cuadruplo[1])
                if self.obtenerValor(direccion) == self.obtenerValor(46001) or self.obtenerValor(direccion) == True:
                    indice = cuadruplo[-1]
                else:
                    indice += 1

            # VERIFICADIM
            elif cuadruplo[0] == 15:
                dir_index = self.obtener_direccion(cuadruplo[1])
                index = self.obtenerValor(dir_index)

                limInf = cuadruplo[2]
                limSup = cuadruplo[3]

                if index <= limSup and index >= limInf:
                    indice += 1
                else:
                    print("Error en Ejecucion- Indice fuera de dimensiones")
                    quit()

            # +DIR
            elif cuadruplo[0] == 16:  # +DIR
                dir_index = self.obtener_direccion(cuadruplo[1])
                dir_base = self.obtener_direccion(cuadruplo[2])
                dir_resultado = self.obtener_direccion(cuadruplo[-1])

                index = self.obtenerValor(dir_index)

                nueva_direccion = dir_base + index + 1

                self.actualizarValor(dir_resultado, nueva_direccion)
                indice += 1

            # <
            elif cuadruplo[0] == 17:
                dir_op1 = self.obtener_direccion(cuadruplo[1])
                dir_op2 = self.obtener_direccion(cuadruplo[2])
                dir_resultado = self.obtener_direccion(cuadruplo[-1])

                op1 = self.obtenerValor(dir_op1)
                op2 = self.obtenerValor(dir_op2)

                resultado = op1 < op2
                if resultado:
                    resultado = self.obtenerValor(46001)
                else:
                    resultado = self.obtenerValor(46000)

                self.actualizarValor(dir_resultado, resultado)
                indice += 1

            # >
            elif cuadruplo[0] == 18:
                dir_op1 = self.obtener_direccion(cuadruplo[1])
                dir_op2 = self.obtener_direccion(cuadruplo[2])
                dir_resultado = self.obtener_direccion(cuadruplo[-1])

                op1 = self.obtenerValor(dir_op1)
                op2 = self.obtenerValor(dir_op2)

                resultado = op1 > op2
                if resultado:
                    resultado = self.obtenerValor(46001)
                else:
                    resultado = self.obtenerValor(46000)

                self.actualizarValor(dir_resultado, resultado)
                indice += 1

            # <>
            elif cuadruplo[0] == 19:
                dir_op1 = self.obtener_direccion(cuadruplo[1])
                dir_op2 = self.obtener_direccion(cuadruplo[2])
                dir_resultado = self.obtener_direccion(cuadruplo[-1])

                op1 = self.obtenerValor(dir_op1)
                op2 = self.obtenerValor(dir_op2)

                resultado = op1 != op2
                if resultado:
                    resultado = self.obtenerValor(46001)
                else:
                    resultado = self.obtenerValor(46000)

                self.actualizarValor(dir_resultado, resultado)
                indice += 1

            elif cuadruplo[0] == 20:  # ==

                dir_op1 = self.obtener_direccion(cuadruplo[1])
                dir_op2 = self.obtener_direccion(cuadruplo[2])
                dir_resultado = self.obtener_direccion(cuadruplo[-1])

                op1 = self.obtenerValor(dir_op1)
                op2 = self.obtenerValor(dir_op2)

                resultado = op1 == op2
                if resultado:
                    resultado = self.obtenerValor(46001)
                else:
                    resultado = self.obtenerValor(46000)

                self.actualizarValor(dir_resultado, resultado)
                indice += 1

            elif cuadruplo[0] == 21:  # ||
                dir_op1 = self.obtener_direccion(cuadruplo[1])
                dir_op2 = self.obtener_direccion(cuadruplo[2])
                dir_resultado = self.obtener_direccion(cuadruplo[-1])

                op1 = self.obtenerValor(dir_op1)
                op2 = self.obtenerValor(dir_op2)

                resultado = op1 == self.obtenerValor(
                    46001) or op2 == self.obtenerValor(46001)
                if resultado:
                    resultado = self.obtenerValor(46001)
                else:
                    resultado = self.obtenerValor(46000)

                self.actualizarValor(dir_resultado, resultado)
                indice += 1

            elif cuadruplo[0] == 22:  # &&
                dir_op1 = self.obtener_direccion(cuadruplo[1])
                dir_op2 = self.obtener_direccion(cuadruplo[2])
                dir_resultado = self.obtener_direccion(cuadruplo[-1])

                op1 = self.obtenerValor(dir_op1)
                op2 = self.obtenerValor(dir_op2)

                resultado = op1 == self.obtenerValor(
                    46001) and op2 == self.obtenerValor(46001)
                if resultado:
                    resultado = self.obtenerValor(46001)
                else:
                    resultado = self.obtenerValor(46000)

                self.actualizarValor(dir_resultado, resultado)
                indice += 1

            elif cuadruplo[0] == 23:  # RET
                self.valorReturn = self.obtenerValor(cuadruplo[-1])
                indice += 1
            else:
                print("CICLOOOOO")
                quit()
