class Cuadruplos:

    def __init__(self):
        self.pilaCuadruplos = {}

    def generarCuadruplo(self, numero, operador, oper_izq, oper_der, resultado):
        self.pilaCuadruplos[numero] = [operador, oper_izq, oper_der, resultado]
        #print(f"Se genero cuadruplo {numero}: {self.pilaCuadruplos[numero]}")

    def imprimir(self):
        f = open("archivoOBJ","a")
        f.write("Cuadruplos \n")
        for numero in self.pilaCuadruplos.keys():
            f.write(f"{numero} : {self.pilaCuadruplos[numero]}")
            f.write("\n")
        f.close()

    def rellenarSalto(self, numero, salto):
        self.pilaCuadruplos[numero][3] = salto
        #print(f"Se relleno cuadruplo {self.pilaCuadruplos[numero]}")
