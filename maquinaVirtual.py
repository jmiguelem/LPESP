

class MaquinaVirtual:
    cuadruplos = []
    codigosOperaciones = {}
    contCuadruplos = 0

    def __init__(self, cuadruplos):
        self.cuadruplos = cuadruplos

    def imprimir_cuadruplos(self):
        for cuadruplo in self.cuadruplos:
            print(f"{self.contCuadruplos} : {cuadruplo}")
            self.contCuadruplos += 1

    def ejecucion(self):

        None
