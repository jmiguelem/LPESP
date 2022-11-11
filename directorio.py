class Directorio:
    def __init__(self):
        self.directorio = {}

    def agregarNuevaFuncion(self, id_funcion, tipo):
        self.directorio[id_funcion] = [tipo, None]

    def crearTablaVariables(self, id_funcion):
        if self.directorio[id_funcion][1] == None:
            tablaVariables = TablaVariables()
            self.directorio[id_funcion][1] = tablaVariables
        else:
            print(f"DEV: Funcion {id_funcion} ya tenia tabla de variables")
        
    def eliminarFuncion(self, id_funcion):
        del self.directorio[id_funcion]

    def eliminarTablaVariables(self, id_funcion):
        del self.directorio[id_funcion][1]
        self.directorio[id_funcion].append(None)

    def imprimirTabla(self):
        print(self.directorio, "\n")
        for funcion in self.directorio.keys():
            print(f"Funcion: {funcion}")
            print(self.directorio[funcion][1].tabla)
            print("\n")

        

class TablaVariables:
    def __init__(self):
        self.tabla = {}

    def crear(self, nombre, tipo):
        if nombre in self.tabla.keys():
            print(f"Error en codigo - Variable: {nombre} ya fue definida")
            exit()
        else:
            self.tabla[nombre] = [tipo, None]

    def regresarTipo(self, nombre):
        try:
            return self.tabla[nombre][0]
        except:
            print("Error en codigo - Variable {nombre} no esta definida ")
            exit() 

    def verificarVariable(self, nombre):
        if nombre in self.tabla.keys():
            pass
        else:
            print(f"Error en codigo - Variable {nombre} no definida")
            exit()
