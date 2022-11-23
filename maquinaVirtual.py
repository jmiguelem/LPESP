from directorio import Directorio
from directorio import Constantes
from directorio import TablaVariables


class MemoriaVirtual:
    def __init__(self):
        self.memoriaVirtual = {}

    def agregar(self, dirMemoria, id, valor):
        if dirMemoria in self.memoriaVirtual.keys():
            print("Ese espacio de memoria ya esta en uso")
            exit()
        else:
            self.memoriaVirtual[dirMemoria] = [id, valor]

    def actualizarValor(self, dirMemoria, valor):
        if dirMemoria in self.memoriaVirtual.keys():
            self.memoriaVirtual[dirMemoria][1] = [valor]
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

    def obtenerValor(self, dirMemoria):
        if dirMemoria in self.memoriaVirtual.keys():
            return self.memoriaVirtual[dirMemoria][1]
        else:
            print("Ese espacio de memoria no existe")
            exit()

    def obtenerId(self, dirMemoria):
        if dirMemoria in self.memoriaVirtual.keys():
            return self.memoriaVirtual[dirMemoria][0]
        else:
            print("Ese espacio de memoria no existe")
            exit()


class MaquinaVirtual:
    cuadruplos = []
    nombrePrograma = ""
    codigosOperaciones = {
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
        'IMPRIME': 14
    }
    directorioFunciones = Directorio()
    tablaConstantes = Constantes()
    memoriaVirtual = MemoriaVirtual()

    def __init__(self, nombrePrograma, cuadruplos, directorio, tablaConstantes):
        self.nombrePrograma = nombrePrograma
        self.cuadruplos = cuadruplos
        self.directorioFunciones = directorio
        self.tablaConstantes = tablaConstantes

    def inicializarCuadruplos(self):
        for cuadruplo in self.cuadruplos:
            if cuadruplo[0] in self.codigosOperaciones:
                cuadruplo[0] = self.codigosOperaciones[cuadruplo[0]]

    def inicializarMemoriaVirtual(self):
        # Tabla Constantes
        for constante in self.tablaConstantes.tablaConstantes:
            self.memoriaVirtual.agregar(
                self.tablaConstantes.tablaConstantes[constante], constante, 4)

        # Tabla Globales
        global tablaVariablesGlobales
        tablaVariablesGlobales = TablaVariables()
        tablaVariablesGlobales = self.directorioFunciones.directorio[self.nombrePrograma][1]
        for variable in tablaVariablesGlobales.tabla:
            self.memoriaVirtual.agregar(
                tablaVariablesGlobales.tabla[variable][1], variable, "")

        # self.memoriaVirtual.imprimirMemoriaVirtual()
        # print(self.memoriaVirtual.obtenerId(30001))
        # self.memoriaVirtual.actualizarValor(30001, "holA")
        # self.memoriaVirtual.imprimirMemoriaVirtual()

    def ejecucion(self):
        self.inicializarMemoriaVirtual()
        self.inicializarCuadruplos()
        for cuadruplo in self.cuadruplos:
            if cuadruplo[0] == 1:
                None
            elif cuadruplo[0] == 2:
                None
            elif cuadruplo[0] == 3:
                None
            elif cuadruplo[0] == 4:
                None
            elif cuadruplo[0] == 5:
                None
            elif cuadruplo[0] == 6:
                None
            elif cuadruplo[0] == 7:
                None
            elif cuadruplo[0] == 8:
                None
            elif cuadruplo[0] == 9:
                None
            elif cuadruplo[0] == 10:
                None
            elif cuadruplo[0] == 11:
                None
            elif cuadruplo[0] == 12:
                None
            elif cuadruplo[0] == 13:
                None
            elif cuadruplo[0] == 14:
                None
