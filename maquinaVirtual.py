from directorio import Directorio
from directorio import Constantes
from directorio import TablaVariables


class MemoriaVirtual:
    def __init__(self):
        self.memoriaVirtual = {}

    def agregar(self, dirMemoria, id, valor):
        if dirMemoria in self.memoriaVirtual.keys():
            print(self.memoriaVirtual)
            print("Ese espacio de memoria ya esta en uso")
            exit()
        else:
            self.memoriaVirtual[dirMemoria] = [id, valor]

    def agregarArre(self, dirMemoria, id, valor, dimension1 = None):
        if dirMemoria in self.memoriaVirtual.keys():
            print(self.memoriaVirtual)
            print("Ese espacio de memoria ya esta en uso")
            exit()
        else:
            self.memoriaVirtual[dirMemoria] = [id, valor, dimension1]

    def agregarMat(self, dirMemoria, id, valor, dimension1 = None, dimension2 = None, desplazo = None):
        if dirMemoria in self.memoriaVirtual.keys():
            print(self.memoriaVirtual)
            print("Ese espacio de memoria ya esta en uso")
            exit()
        else:
            self.memoriaVirtual[dirMemoria] = [id, valor, dimension1, dimension2, desplazo]

    def actualizarValor(self, dirMemoria, valor):
        if dirMemoria in self.memoriaVirtual.keys():
            self.memoriaVirtual[dirMemoria][1] = valor
        else:
            if dirMemoria >= 200000:
                self.agregar(dirMemoria,"", valor )
            else :
                print(self.memoriaVirtual)
                print("Ese espacio de memoria no existe")
                exit()

    def actualizarId(self, dirMemoria, id):
        if dirMemoria in self.memoriaVirtual.keys():
            self.memoriaVirtual[dirMemoria][0] = [id]
        else:
            print(self.memoriaVirtual)
            print("Ese espacio de memoria no existe")
            exit()

    def imprimirMemoriaVirtual(self):
        for memoria in self.memoriaVirtual:
            print("[", memoria, self.memoriaVirtual[memoria]
                  [0], self.memoriaVirtual[memoria][1], "]")

    def obtenerValor(self, dirMemoria):
        if dirMemoria in self.memoriaVirtual.keys():
            if self.memoriaVirtual[dirMemoria][1] == '':
                print(f"Error en Ejecucion- Vairable {self.memoriaVirtual[dirMemoria][0]} no tiene asignado un valor")
                quit()

            return self.memoriaVirtual[dirMemoria][1]
        else:
            if dirMemoria >= 200000:
                self.agregar(dirMemoria,"","" )
            else:
                print(f"Espacio {dirMemoria} de memoria no existe")
                print(self.memoriaVirtual)
                exit()

    def obtenerLen(self, dirMemoria):
        return len(self.memoriaVirtual[dirMemoria])

    def obtenerDimArreglo(self, dirMemoria):
        return self.memoriaVirtual[dirMemoria][2]

    def obtenerDimMatriz(self, dirMemoria):
        return self.memoriaVirtual[dirMemoria][4]

    def obtenerId(self, dirMemoria):
        if dirMemoria in self.memoriaVirtual.keys():
            return self.memoriaVirtual[dirMemoria][0]
        else:
            print("Ese espacio de memoria no existe")
            print(self.memoriaVirtual)
            exit()


class MaquinaVirtual:
    cuadruplos = []
    nombrePrograma = ""
    migajas = []
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
        '&&': 22
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
            print(f"{indice} : {pila[indice]}")
            cuadruplo = pila[indice]
            if cuadruplo[0] in self.codigosOperaciones:
                self.cuadruplos.pilaCuadruplos[indice][0] = self.codigosOperaciones[cuadruplo[0]]

        print(self.cuadruplos.pilaCuadruplos)

    def validarTipo(self, direccion):
        pass

    def debug(self, indice):
        print(f"Corriendo cuaduplo: {indice}")

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
                    self.memoriaVirtual.agregar(dir+i + 1, f"{variable}{i}", "")

            elif len(tablaVariablesGlobales.tabla[variable]) == 5:
                dir = tablaVariablesGlobales.tabla[variable][1]
                dim = tablaVariablesGlobales.tabla[variable][4]

                self.memoriaVirtual.agregarMat(
                    dir, variable, "OBJETO DE MATRIZ",tablaVariablesGlobales.tabla[variable][2],tablaVariablesGlobales.tabla[variable][3], dim)

                for i in range(dim):
                    self.memoriaVirtual.agregar(dir+i+1, f"{variable}{i}", "")
                    
            else:
                self.memoriaVirtual.agregar(
                tablaVariablesGlobales.tabla[variable][1], variable, "")
            

        #self.memoriaVirtual.imprimirMemoriaVirtual()
        # print(self.memoriaVirtual.obtenerId(30001))
        # self.memoriaVirtual.actualizarValor(30001, "holA")
        # self.memoriaVirtual.imprimirMemoriaVirtual()

    def ejecucion(self):
        memoria = self.memoriaVirtual
        pila = self.cuadruplos.pilaCuadruplos
        indice = 1
        while indice <= len(pila):
            cuadruplo = pila[indice]
            #print("\n")
            #self.debug(indice)
            #print(cuadruplo)
            #memoria.imprimirMemoriaVirtual()

            if cuadruplo[0] == 0:  # GOTOMAIN
                indice = cuadruplo[-1]

            elif cuadruplo[0] == 1:  # ASIGNACION
                try:
                    direccion = cuadruplo[1]
                    valor = memoria.obtenerValor(direccion)
                except:
                    pass

                if type(cuadruplo[-1]) == type(""):
                    direccion = int(cuadruplo[-1][1:-1])
                    direccion_arreglo = memoria.obtenerValor(direccion)
                    valor = memoria.obtenerValor(cuadruplo[1])
                    memoria.actualizarValor(direccion_arreglo, valor)
                    indice += 1
                elif type(cuadruplo[1]) == type(""):
                    dir_valor = int(cuadruplo[1][1:-1])
                    valor = memoria.obtenerValor(dir_valor)
                    valor = memoria.obtenerValor(valor) #1
                    direccion = cuadruplo[-1]
                    memoria.actualizarValor(direccion, valor)
                    indice += 1
                else:
                    if cuadruplo[-1] >= 1000 and cuadruplo[-1] < 5000:
                        try:
                            valor = int(valor)
                        except:
                            print(f"Error de Ejecucion - se esta tratando de asignar un tipo de dato incorrecto a: {variable}")
                            quit()
                    elif cuadruplo[-1] >= 5000 and cuadruplo[-1] < 9000:
                        try:
                            valor = float(valor)
                        except:
                            print(f"Error de Ejecucion - se esta tratando de asignar un tipo de dato incorrecto a: {variable}")
                            quit()
                    elif cuadruplo[-1] >= 9000 and cuadruplo[-1] < 13000:
                        try:
                            valor = str(valor)
                        except:
                            print(f"Error de Ejecucion - se esta tratando de asignar un tipo de dato incorrecto a: {variable}")
                            quit()
                    memoria.actualizarValor(cuadruplo[-1], valor)
                    indice += 1

            elif cuadruplo[0] == 2:  # SUMA
                dir_op1 = cuadruplo[1]
                op1 = memoria.obtenerValor(dir_op1)

                dir_op2 = cuadruplo[2]
                op2 = memoria.obtenerValor(dir_op2)

                resultado = op1 + op2
                dir_resultado = cuadruplo[-1]

                memoria.actualizarValor(dir_resultado, resultado)
                indice += 1

            elif cuadruplo[0] == 3:  # RESTA
                dir_op1 = cuadruplo[1]
                op1 = memoria.obtenerValor(dir_op1)

                dir_op2 = cuadruplo[2]
                op2 = memoria.obtenerValor(dir_op2)

                resultado = op1 - op2
                dir_resultado = cuadruplo[-1]

                memoria.actualizarValor(dir_resultado, resultado)
                indice += 1

            elif cuadruplo[0] == 4:  # Multiplicacion
                dir_op1 = cuadruplo[1]
                op1 = memoria.obtenerValor(dir_op1)

                dir_op2 = cuadruplo[2]
                op2 = memoria.obtenerValor(dir_op2)

                resultado = op1 * op2
                dir_resultado = cuadruplo[-1]

                memoria.actualizarValor(dir_resultado, resultado)
                indice += 1

            elif cuadruplo[0] == 5:  # DIVISION
                dir_op1 = cuadruplo[1]
                op1 = memoria.obtenerValor(dir_op1)

                dir_op2 = cuadruplo[2]
                op2 = memoria.obtenerValor(dir_op2)

                resultado = op1 / op2
                dir_resultado = cuadruplo[-1]

                memoria.actualizarValor(dir_resultado, resultado)
                indice += 1

            elif cuadruplo[0] == 6:  # ENDFUNC
                indice = self.migajas.pop()

            elif cuadruplo[0] == 7:  # ERA
                # CARGAR MEMORIA LOCAL
                indice += 1

            elif cuadruplo[0] == 8:  # PARAMETER

                indice += 1

            elif cuadruplo[0] == 9:  # GOSUB
                indice += 1

            elif cuadruplo[0] == 10:  # IMPRIME
                direccion = cuadruplo[-1]
                leng = memoria.obtenerLen(direccion)
                if leng == 3:
                    dim = memoria.obtenerDimArreglo(direccion)
                    arreglo = '['
                    for i in range(dim):
                        arreglo += str(memoria.obtenerValor(direccion + i + 1))
                    arreglo += "]"
                    print(arreglo)

                elif leng == 5:
                    dim = memoria.obtenerDimMatriz(direccion)
                    arreglo = '['
                    for i in range(dim):
                        arreglo += str(memoria.obtenerValor(direccion + i + 1))
                    arreglo += "]"
                    print(arreglo)
                else:
                    valor = memoria.obtenerValor(direccion)
                    print(valor)
                indice += 1

            elif cuadruplo[0] == 11:  # LEER
                variable = memoria.obtenerId(cuadruplo[-1])
                valor = input(f"Ingresa el valor de {variable}: ")
                if cuadruplo[-1] >= 1000 and cuadruplo[-1] < 5000:
                    try:
                        valor = int(valor)
                    except:
                        print(f"Error de Ejecucion - se esta tratando de asignar un tipo de dato incorrecto a: {variable}")
                        quit()
                elif cuadruplo[-1] >= 5000 and cuadruplo[-1] < 9000:
                    try:
                        valor = float(valor)
                    except:
                        print(f"Error de Ejecucion - se esta tratando de asignar un tipo de dato incorrecto a: {variable}")
                        quit()
                elif cuadruplo[-1] >= 9000 and cuadruplo[-1] < 13000:
                    try:
                        valor = str(valor)
                    except:
                        print(f"Error de Ejecucion - se esta tratando de asignar un tipo de dato incorrecto a: {variable}")
                        quit()
                memoria.actualizarValor(cuadruplo[-1],valor)
                indice += 1

            elif cuadruplo[0] == 12:  # GOTOF
                if memoria.obtenerValor(cuadruplo[1]) == "FALSO" or memoria.obtenerValor(cuadruplo[1]) == False:
                    indice = cuadruplo[-1]
                else:
                    indice += 1

            elif cuadruplo[0] == 13:  # GOTO
                indice = cuadruplo[-1]

            elif cuadruplo[0] == 14:  # GOTOT
                if memoria.obtenerValor(cuadruplo[1]) == "VERDADERO" or memoria.obtenerValor(cuadruplo[1]) == True:
                    indice = cuadruplo[-1]
                else:
                    indice += 1

            elif cuadruplo[0] == 15:  # VERIFICADIM
                dir_index = cuadruplo[1]
                index = memoria.obtenerValor(dir_index)
                limInf = cuadruplo[2]
                limSup = cuadruplo[3]
                if index <= limSup and index >= limInf:
                    indice += 1
                else:
                    print("Error en Ejecucion- Indice fuera de dimensiones")
                    quit()

            elif cuadruplo[0] == 16:  # +DIR
                dir_indice = cuadruplo[1]
                index = memoria.obtenerValor(dir_indice)
                dir_base = cuadruplo[2]
                nueva_direccion = dir_base + index + 1
                resultado = cuadruplo[-1]
                memoria.actualizarValor(resultado, nueva_direccion)
                indice += 1

            elif cuadruplo[0] == 17:  # <
                dir_op1 = cuadruplo[1]
                op1 = memoria.obtenerValor(dir_op1)
                dir_op2 = cuadruplo[2]
                op2 = memoria.obtenerValor(dir_op2)
                res = op1 < op2
                memoria.actualizarValor(cuadruplo[-1], res)
                indice += 1

            elif cuadruplo[0] == 18:  # >
                dir_op1 = cuadruplo[1]
                op1 = memoria.obtenerValor(dir_op1)
                dir_op2 = cuadruplo[2]
                op2 = memoria.obtenerValor(dir_op2)
                res = op1 > op2
                memoria.actualizarValor(cuadruplo[-1], res)
                indice += 1

            elif cuadruplo[0] == 19:  # <>
                dir_op1 = cuadruplo[1]
                op1 = memoria.obtenerValor(dir_op1)
                dir_op2 = cuadruplo[2]
                op2 = memoria.obtenerValor(dir_op2)
                res = op1 != op2
                memoria.actualizarValor(cuadruplo[-1], res)
                indice += 1

            elif cuadruplo[0] == 20:  # ==
                dir_op1 = cuadruplo[1]
                op1 = memoria.obtenerValor(dir_op1)
                dir_op2 = cuadruplo[2]
                op2 = memoria.obtenerValor(dir_op2)
                res = op1 < op2
                memoria.actualizarValor(cuadruplo[-1], res)
                indice += 1

            elif cuadruplo[0] == 21:  # ||
                dir_op1 = cuadruplo[1]
                op1 = memoria.obtenerValor(dir_op1)
                dir_op2 = cuadruplo[2]
                op2 = memoria.obtenerValor(dir_op2)
                res = op1 or  op2
                memoria.actualizarValor(cuadruplo[-1], res)
                indice += 1

            elif cuadruplo[0] == 22:  # &&
                dir_op1 = cuadruplo[1]
                op1 = memoria.obtenerValor(dir_op1)
                dir_op2 = cuadruplo[2]
                op2 = memoria.obtenerValor(dir_op2)
                res = op1 and op2
                memoria.actualizarValor(cuadruplo[-1], res)
                indice += 1
            else:
                print("CICLOOOOO")
                quit()
