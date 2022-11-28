
class MemoriaVirtual:
    def __init__(self):
        self.memoriaVirtual = {}

    def agregar(self, dirMemoria, id, valor):
        if dirMemoria in self.memoriaVirtual.keys():
            print("Ese espacio de memoria ya esta en uso (agregar)",
                  dirMemoria, id, valor)
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
            if dirMemoria >= 50000:
                self.agregar(dirMemoria, "", valor)
            else:
                print(dirMemoria, valor,
                      "Ese espacio de memoria no existe (actualizarValor)")
                exit()

    def actualizarId(self, dirMemoria, id):
        if dirMemoria in self.memoriaVirtual.keys():
            self.memoriaVirtual[dirMemoria][0] = [id]
        else:
            print("Ese espacio de memoria no existe (actualizarId)")
            exit()

    def imprimirMemoriaVirtual(self):
        for memoria in self.memoriaVirtual:
            print("[", memoria, self.memoriaVirtual[memoria]
                  [0], self.memoriaVirtual[memoria][1], "]")

    def checarExistenciaValor(self, dirMemoria):
        if dirMemoria in self.memoriaVirtual.keys():
            return True
        else:
            if dirMemoria >= 50000:
                self.agregar(dirMemoria, "", "")
            else:
                return False

    def obtenerValor(self, dirMemoria):
        if dirMemoria in self.memoriaVirtual.keys():
            if self.memoriaVirtual[dirMemoria][1] == '':
                print(dirMemoria,
                      f"Error en Ejecucion- Variable {self.memoriaVirtual[dirMemoria][0]} no tiene asignado un valor")
                quit()

            return self.memoriaVirtual[dirMemoria][1]
        else:
            if dirMemoria >= 50000:
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
            print("Ese espacio de memoria no existe (obtenerId)")
            exit()

    def borrarMemoria(self):
        self.memoriaVirtual = {}
