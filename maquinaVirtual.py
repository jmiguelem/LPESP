from directorio import Directorio
from directorio import Constantes
from directorio import TablaVariables


class MemoriaVirtual:
    def __init__(self):
        self.memoriaVirtual = {}

    def agregar(self, dirMemoria, id, valor):
        if dirMemoria in self.memoriaVirtual.keys():
            print("Ese espacio de memoria ya esta en uso", dirMemoria)
            exit()
        else:
            self.memoriaVirtual[dirMemoria] = [id, valor]

    def agregarArre(self, dirMemoria, id, valor, dimension1=None):
        if dirMemoria in self.memoriaVirtual.keys():
            print(self.memoriaVirtual)
            print("Ese espacio de memoria ya esta en uso (agregarArre)", dirMemoria)
            exit()
        else:
            self.memoriaVirtual[dirMemoria] = [id, valor, dimension1]

    def agregarMat(self, dirMemoria, id, valor, dimension1=None, dimension2=None, desplazo=None):
        if dirMemoria in self.memoriaVirtual.keys():
            print(self.memoriaVirtual)
            print("Ese espacio de memoria ya esta en uso (agregaMatriz)", dirMemoria)
            exit()
        else:
            self.memoriaVirtual[dirMemoria] = [
                id, valor, dimension1, dimension2, desplazo]

    def actualizarValor(self, dirMemoria, valor):
        if dirMemoria in self.memoriaVirtual.keys():
            self.memoriaVirtual[dirMemoria][1] = valor
        else:
            if dirMemoria >= 200000:
                self.agregar(dirMemoria, "", valor)
            else:
                print("Ese espacio de memoria no existe")
                exit()

    def actualizarId(self, dirMemoria, id):
        if dirMemoria in self.memoriaVirtual.keys():
            self.memoriaVirtual[dirMemoria][0] = [id]
        else:
            print("Ese espacio de memoria no existe")
            exit()

    def imprimirMemoriaVirtual(self):
        for memoria in self.memoriaVirtual:
            print("[", memoria, self.memoriaVirtual[memoria]
                  [0], self.memoriaVirtual[memoria][1], "]")

    def checarExistenciaValor(self, dirMemoria):
        if dirMemoria in self.memoriaVirtual.keys():
            return True
        else:
            if dirMemoria >= 200000:
                self.agregar(dirMemoria, "", "")
            else:
                return False

    def obtenerValor(self, dirMemoria):
        if dirMemoria in self.memoriaVirtual.keys():
            if self.memoriaVirtual[dirMemoria][1] == '':
                print(
                    f"Error en Ejecucion- Variable {self.memoriaVirtual[dirMemoria][0]} no tiene asignado un valor")
                quit()

            return self.memoriaVirtual[dirMemoria][1]
        else:
            if dirMemoria >= 200000:
                self.agregar(dirMemoria, "", "")
            else:
                print(f"Espacio {dirMemoria} de memoria no existe")
                exit()

    def obtenerLen(self, dirMemoria):
        return len(self.memoriaVirtual[dirMemoria])

    def obtenerDimArreglo(self, dirMemoria):
        return self.memoriaVirtual[dirMemoria][2]

    def obtenerDimMatriz(self, dirMemoria):
        return self.memoriaVirtual[dirMemoria][4]

    def obtenerDims(self, dirMemoria):
        return self.memoriaVirtual[dirMemoria][2], self.memoriaVirtual[dirMemoria][3]

    def obtenerId(self, dirMemoria):
        if dirMemoria in self.memoriaVirtual.keys():
            return self.memoriaVirtual[dirMemoria][0]
        else:
            print("Ese espacio de memoria no existe")
            exit()


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
    memoriaVirtual = MemoriaVirtual()

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

    def validarTipo(self, direccion):
        pass

    def debug(self, indice):
        print(f"Corriendo cuaduplo: {indice}")

    def crearMemoriaLocal(self, nombre_funcion):
        # Tabla Locales
        global tablaVariablesLocales
        tablaVariablesLocales = TablaVariables()
        tablaVariablesLocales = self.directorioFunciones.directorio[nombre_funcion][1]

        global memoriaLocal
        memoriaLocal = MemoriaVirtual()

        #numeroParams = self.directorioFunciones.directorio[nombre_funcion][3]
        #numeroVars = self.directorioFunciones.directorio[nombre_funcion][4]

        for variableLocal in tablaVariablesLocales.tabla:
            if len(tablaVariablesLocales.tabla[variableLocal]) == 3:
                dir = tablaVariablesLocales.tabla[variableLocal][1]
                dim = tablaVariablesLocales.tabla[variableLocal][2]

                self.memoriaVirtual.agregarArre(
                    dir, variableLocal, "OBJETO DE ARREGLO", dim)

                for i in range(dim):
                    self.memoriaVirtual.agregar(
                        dir+i + 1, f"{variableLocal}{i}", "")

            elif len(tablaVariablesLocales.tabla[variableLocal]) == 5:
                dir = tablaVariablesLocales.tabla[variableLocal][1]
                dim = tablaVariablesLocales.tabla[variableLocal][4]

                self.memoriaVirtual.agregarMat(
                    dir, variableLocal, "OBJETO DE ARREGLO", tablaVariablesLocales.tabla[variableLocal][2], tablaVariablesLocales.tabla[variableLocal][3], dim)

                for i in range(dim):
                    self.memoriaVirtual.agregar(
                        dir+i+1, f"{variableLocal}{i}", "")

            else:
                self.memoriaVirtual.agregar(
                    tablaVariablesLocales.tabla[variableLocal][1], variableLocal, "")

    def inicializarMemoriaVirtual(self):
        # Tabla Constantes
        for constante in self.tablaConstantes.tablaConstantes:
            self.memoriaVirtual.agregar(
                self.tablaConstantes.tablaConstantes[constante], constante, constante)

        # Tabla Globales
        global tablaVariablesGlobales
        tablaVariablesGlobales = TablaVariables()
        tablaVariablesGlobales = self.directorioFunciones.directorio[self.nombrePrograma][1]

        for variable in tablaVariablesGlobales.tabla:

            if len(tablaVariablesGlobales.tabla[variable]) == 3:
                dir = tablaVariablesGlobales.tabla[variable][1]
                dim = tablaVariablesGlobales.tabla[variable][2]

                self.memoriaVirtual.agregarArre(
                    dir, variable, "OBJETO DE ARREGLO", dim)

                for i in range(dim):
                    self.memoriaVirtual.agregar(
                        dir+i + 1, f"{variable}{i}", "")

            elif len(tablaVariablesGlobales.tabla[variable]) == 5:
                dir = tablaVariablesGlobales.tabla[variable][1]
                dim = tablaVariablesGlobales.tabla[variable][4]

                self.memoriaVirtual.agregarMat(
                    dir, variable, "OBJETO DE MATRIZ", tablaVariablesGlobales.tabla[variable][2], tablaVariablesGlobales.tabla[variable][3], dim)

                for i in range(dim):
                    self.memoriaVirtual.agregar(dir+i+1, f"{variable}{i}", "")

            else:
                self.memoriaVirtual.agregar(
                    tablaVariablesGlobales.tabla[variable][1], variable, "")

    def obtener_direccion(self, direccion):
        memoria = self.memoriaVirtual
        if type(direccion) == type(' '):
            apuntador = int(direccion[1:-1])
            dir_arreglo = memoria.obtenerValor(apuntador)
            return dir_arreglo
        else:
            return direccion



    def ejecucion(self):
        memoria = self.memoriaVirtual
        pila = self.cuadruplos.pilaCuadruplos
        indice = 1
        while indice <= len(pila):
            cuadruplo = pila[indice]
            #print(f"{indice}: {cuadruplo}")
            #memoria.imprimirMemoriaVirtual()
            
            #GOTO MAIN
            if cuadruplo[0] == 0:
                indice = cuadruplo[-1]

            # ASIGNACION
            elif cuadruplo[0] == 1:
                direccion_op1 = self.obtener_direccion(cuadruplo[1])
                valor = memoria.obtenerValor(direccion_op1)

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
                memoria.actualizarValor(direccion_op2, valor)
                indice += 1

            #SUMA
            elif cuadruplo[0] == 2:
                direccion_op1 = self.obtener_direccion(cuadruplo[1])
                direccion_op2 = self.obtener_direccion(cuadruplo[2])
                direccion_resultado = self.obtener_direccion(cuadruplo[-1])

                op1 = memoria.obtenerValor(direccion_op1)
                op2 = memoria.obtenerValor(direccion_op2)

                resultado = op1 + op2

                memoria.actualizarValor(direccion_resultado, resultado)
                indice += 1

            #RESTA
            elif cuadruplo[0] == 3:
                direccion_op1 = self.obtener_direccion(cuadruplo[1])
                direccion_op2 = self.obtener_direccion(cuadruplo[2])
                direccion_resultado = self.obtener_direccion(cuadruplo[-1])

                op1 = memoria.obtenerValor(direccion_op1)
                op2 = memoria.obtenerValor(direccion_op2)

                resultado = op1 - op2

                memoria.actualizarValor(direccion_resultado, resultado)
                indice += 1

            #MULTIPLICACION
            elif cuadruplo[0] == 4:
                direccion_op1 = self.obtener_direccion(cuadruplo[1])
                direccion_op2 = self.obtener_direccion(cuadruplo[2])
                direccion_resultado = self.obtener_direccion(cuadruplo[-1])

                op1 = memoria.obtenerValor(direccion_op1)
                op2 = memoria.obtenerValor(direccion_op2)

                resultado = op1 * op2

                memoria.actualizarValor(direccion_resultado, resultado)
                indice += 1

            #DIVISION
            elif cuadruplo[0] == 5:
                direccion_op1 = self.obtener_direccion(cuadruplo[1])
                direccion_op2 = self.obtener_direccion(cuadruplo[2])
                direccion_resultado = self.obtener_direccion(cuadruplo[-1])

                op1 = memoria.obtenerValor(direccion_op1)
                op2 = memoria.obtenerValor(direccion_op2)

                try:
                    resultado = op1 / op2
                except:
                    print("Error - Error al hacer la division. Verifica valor de operadores")

                memoria.actualizarValor(direccion_resultado, resultado)
                indice += 1

            elif cuadruplo[0] == 6:  # ENDFUNC
                indice_temp = self.migajas.pop()
                cuadruplo = pila[indice_temp]
                memoria.actualizarValor(cuadruplo[1], self.valorReturn)
                indice = indice_temp

            elif cuadruplo[0] == 7:  # ERA
                # CARGAR MEMORIA LOCAL
                self.crearMemoriaLocal(cuadruplo[-1])
                indice += 1

            elif cuadruplo[0] == 8:  # PARAMETER
                direccion = self.obtener_direccion(cuadruplo[1])
                valor = memoria.obtenerValor(direccion)
                if cuadruplo[-1] >= 10000 and cuadruplo[-1] < 50000:
                    try:
                        valor = int(valor)
                    except:
                        print(
                            f"Error de Ejecucion - se esta tratando de asignar un tipo de dato incorrecto a: {variable}")
                        quit()
                elif cuadruplo[-1] >= 50000 and cuadruplo[-1] < 90000:
                    try:
                        valor = float(valor)
                    except:
                        print(
                            f"Error de Ejecucion - se esta tratando de asignar un tipo de dato incorrecto a: {variable}")
                        quit()
                elif cuadruplo[-1] >= 90000 and cuadruplo[-1] < 130000:
                    try:
                        valor = str(valor)
                    except:
                        print(
                            f"Error de Ejecucion - se esta tratando de asignar un tipo de dato incorrecto a: {variable}")
                        quit()
                memoria.actualizarValor(cuadruplo[-1], valor)

                indice += 1

            elif cuadruplo[0] == 9:  # GOSUB
                self.migajas.append(indice + 1)
                indice = cuadruplo[-1]

            #IMPRIME
            elif cuadruplo[0] == 10:
                direccion = self.obtener_direccion(cuadruplo[-1])
                length = memoria.obtenerLen(direccion)

                if length == 3:
                        dim = memoria.obtenerDimArreglo(direccion)
                        valor = '['
                        for i in range(dim):
                            valor += str(memoria.obtenerValor(direccion + i + 1)) + " "
                        valor = valor[: -1]
                        valor += "]"
                
                elif length == 5:
                        dim1, dim2 = memoria.obtenerDims(direccion)
                        dim = memoria.obtenerDimMatriz(direccion)
                        valor = '[ \n'
                        i = 0
                        for j in range(dim1):
                            for k in range(dim2):
                                valor += str(memoria.obtenerValor(direccion + i + 1)) + " "
                                i += 1
                            valor += "\n"
                        valor += "]"

                else:
                    valor = memoria.obtenerValor(direccion)

                print(valor)
                indice += 1

            #LEER
            elif cuadruplo[0] == 11:
                variable = memoria.obtenerId(cuadruplo[-1])
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
                memoria.actualizarValor(cuadruplo[-1], valor)
                indice += 1

            #GOTOF
            elif cuadruplo[0] == 12:
                direccion = self.obtener_direccion(cuadruplo[1])
                if memoria.obtenerValor(direccion) == memoria.obtenerValor(36000) or memoria.obtenerValor(direccion) == False:
                    indice = cuadruplo[-1]
                else:
                    indice += 1

            #GOTO
            elif cuadruplo[0] == 13:
                indice = cuadruplo[-1]

            #GOTOT
            elif cuadruplo[0] == 14:
                direccion = self.obtener_direccion(cuadruplo[1])
                if memoria.obtenerValor(direccion) == memoria.obtenerValor(36001) or memoria.obtenerValor(direccion) == True:
                    indice = cuadruplo[-1]
                else:
                    indice += 1

            # VERIFICADIM
            elif cuadruplo[0] == 15:
                dir_index = self.obtener_direccion(cuadruplo[1])
                index = memoria.obtenerValor(dir_index)

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

                index = memoria.obtenerValor(dir_index)
                
                nueva_direccion = dir_base + index + 1

                memoria.actualizarValor(dir_resultado, nueva_direccion)
                indice += 1

            # <
            elif cuadruplo[0] == 17:
                dir_op1 = self.obtener_direccion(cuadruplo[1])
                dir_op2 = self.obtener_direccion(cuadruplo[2])
                dir_resultado = self.obtener_direccion(cuadruplo[-1])

                op1 = memoria.obtenerValor(dir_op1)
                op2 = memoria.obtenerValor(dir_op2)

                resultado =  op1 < op2
                if resultado:
                    resultado = memoria.obtenerValor(36001)
                else:
                    resultado = memoria.obtenerValor(36000)

                memoria.actualizarValor(dir_resultado, resultado)
                indice += 1

            # >
            elif cuadruplo[0] == 18:
                dir_op1 = self.obtener_direccion(cuadruplo[1])
                dir_op2 = self.obtener_direccion(cuadruplo[2])
                dir_resultado = self.obtener_direccion(cuadruplo[-1])

                op1 = memoria.obtenerValor(dir_op1)
                op2 = memoria.obtenerValor(dir_op2)

                resultado =  op1 > op2
                if resultado:
                    resultado = memoria.obtenerValor(36001)
                else:
                    resultado = memoria.obtenerValor(36000)

                memoria.actualizarValor(dir_resultado, resultado)
                indice += 1

            # <>
            elif cuadruplo[0] == 19:
                dir_op1 = self.obtener_direccion(cuadruplo[1])
                dir_op2 = self.obtener_direccion(cuadruplo[2])
                dir_resultado = self.obtener_direccion(cuadruplo[-1])

                op1 = memoria.obtenerValor(dir_op1)
                op2 = memoria.obtenerValor(dir_op2)

                resultado =  op1 != op2
                if resultado:
                    resultado = memoria.obtenerValor(36001)
                else:
                    resultado = memoria.obtenerValor(36000)

                memoria.actualizarValor(dir_resultado, resultado)
                indice += 1

            elif cuadruplo[0] == 20:  # ==

                dir_op1 = self.obtener_direccion(cuadruplo[1])
                dir_op2 = self.obtener_direccion(cuadruplo[2])
                dir_resultado = self.obtener_direccion(cuadruplo[-1])

                op1 = memoria.obtenerValor(dir_op1)
                op2 = memoria.obtenerValor(dir_op2)

                resultado =  op1 == op2
                if resultado:
                    resultado = memoria.obtenerValor(36001)
                else:
                    resultado = memoria.obtenerValor(36000)

                memoria.actualizarValor(dir_resultado, resultado)
                indice += 1

            elif cuadruplo[0] == 21:  # ||
                dir_op1 = self.obtener_direccion(cuadruplo[1])
                dir_op2 = self.obtener_direccion(cuadruplo[2])
                dir_resultado = self.obtener_direccion(cuadruplo[-1])

                op1 = memoria.obtenerValor(dir_op1)
                op2 = memoria.obtenerValor(dir_op2)

                resultado =  op1 == memoria.obtenerValor(
                        36001) or op2 == memoria.obtenerValor(36001)
                if resultado:
                    resultado = memoria.obtenerValor(36001)
                else:
                    resultado = memoria.obtenerValor(36000)

                memoria.actualizarValor(dir_resultado, resultado)
                indice += 1

            elif cuadruplo[0] == 22:  # &&
                dir_op1 = self.obtener_direccion(cuadruplo[1])
                dir_op2 = self.obtener_direccion(cuadruplo[2])
                dir_resultado = self.obtener_direccion(cuadruplo[-1])

                op1 = memoria.obtenerValor(dir_op1)
                op2 = memoria.obtenerValor(dir_op2)

                resultado =  op1 == memoria.obtenerValor(
                        36001) and op2 == memoria.obtenerValor(36001)
                if resultado:
                    resultado = memoria.obtenerValor(36001)
                else:
                    resultado = memoria.obtenerValor(36000)

                memoria.actualizarValor(dir_resultado, resultado)
                indice += 1

            
            elif cuadruplo[0] == 23:  # RET
                self.valorReturn = memoria.obtenerValor(cuadruplo[-1])
                indice += 1
            else:
                print("CICLOOOOO")
                quit()
