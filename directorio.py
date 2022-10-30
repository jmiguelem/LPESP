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

        

class TablaVariables:
    def __init__(self):
        self.tabla = {}

    def crear(self, nombre, tipo):
        if nombre in self.tabla.keys():
            print(f"Error en codigo \n Variable: {nombre} ya fue definida")
            exit()
        else:
            self.tabla[nombre] = [tipo, None]