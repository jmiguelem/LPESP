from directorio import Directorio
from directorio import Constantes


class MaquinaVirtual:
    cuadruplos = []
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

    def __init__(self, cuadruplos, directorio, tablaConstantes):
        self.cuadruplos = cuadruplos
        self.directorioFunciones = directorio
        self.tablaConstantes = tablaConstantes

    def inicializarCuadruplos(self):
        for cuadruplo in self.cuadruplos:
            if cuadruplo[0] in self.codigosOperaciones:
                cuadruplo[0] = self.codigosOperaciones[cuadruplo[0]]

    def ejecucion(self):

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
                print()
