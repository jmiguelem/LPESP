class Cuadruplos:
    
    def __init__(self):
        self.pilaCuadruplos = []

    def generarCaudruplo(self, operador, oper_izq, oper_der, resultado):
        self.pilaCuadruplos.append([operador, oper_izq, oper_der, resultado])

    def imprimir(self):
        print("\n CUADRUPLOS CON DRECCIONES")
        contador = 1
        for cuadruplo in self.pilaCuadruplos:
            print(f"{contador} : {cuadruplo}")
            contador += 1