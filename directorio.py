class Directorio:
    def __init__(self):
        self.directorio = {}
        self.tablaVariablesLocales = TablaVariables()

    def agregarNuevaFuncion(self, id_funcion, tipo):
        # [key] = [tipo_retorno, tabla_variables, tipo_parametros, numero_parametros, numero_variables_locales, numero_de_cuadruplo]
        self.directorio[id_funcion] = [tipo, None, None, 0, 0, 0]

    def agregarTipoParametrosFuncion(self, id_funcion, tipo_param):
        arregloTipoParametrosFuncion = self.directorio[id_funcion][2]
        arregloTipoParametrosFuncion.append(tipo_param)
        self.directorio[id_funcion][2] = arregloTipoParametrosFuncion
        # Sumar numero parametros contador
        self.contadorNuevoParametro(id_funcion)

    def crearArregloTiposParam(self, id_funcion):
        self.directorio[id_funcion][2] = []

    def crearTablaVariables(self, id_funcion):
        if self.directorio[id_funcion][1] == None:
            tablaVariables = TablaVariables()
            self.directorio[id_funcion][1] = tablaVariables
        else:
            print(f"DEV: Funcion {id_funcion} ya tenia tabla de variables")

    def asignarTablaVariablesLocales(self, id_funcion):
        if self.directorio[id_funcion][1] == None:
            self.directorio[id_funcion][1] = self.tablaVariablesLocales
        else:
            print(
                f"DEV: Funcion {id_funcion} ya tenia tabla de variables locales")

    def limpiarTablaVariablesLocales(self, id_funcion):
        self.tablaVariablesLocales.limpiarTabla()
        self.directorio[id_funcion][1] = self.tablaVariablesLocales

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

    def contadorNuevoParametro(self, id_funcion):
        totalParametros = self.directorio[id_funcion][3]
        totalParametros += 1
        self.directorio[id_funcion][3] = totalParametros

    def contadorNuevaVariableLocal(self, id_funcion):
        totalVariablesLocales = self.directorio[id_funcion][4]
        totalVariablesLocales += 1
        self.directorio[id_funcion][4] = totalVariablesLocales

    def guardarContadorCuadruplos(self, id_funcion, numero_cuadruplo):
        self.directorio[id_funcion][5] = numero_cuadruplo

    def verificarFuncionExiste(self, id_funcion):
        try:
            return self.directorio[id_funcion]
        except:
            print(f"La funcion: {id_funcion} no esta definida")
            exit()


class TablaVariables:
    def __init__(self):
        self.tabla = {}

    def crear(self, nombre, tipo, direccion, esArreglo=False):
        if nombre in self.tabla.keys():
            print(f"Error en codigo - Variable: {nombre} ya fue definida")
            exit()
        else:
            if esArreglo:
                self.tabla[nombre] = [tipo, direccion, 0]
                print(f"Se creo variable {nombre} con {self.tabla[nombre]}")
            else:
                self.tabla[nombre] = [tipo, direccion]
                print(f"Se creo variable {nombre} con {self.tabla[nombre]}")

    def regresarTipo(self, nombre):
        try:
            return self.tabla[nombre][0]
        except:
            print(f"Error en codigo - Variable {nombre} no esta definida ")
            exit()

    def regresarDireccion(self, nombre):
        try:
            return self.tabla[nombre][1]
        except:
            print(
                f"Error en codigo -  Direccion de  {nombre} no esta definida")
            exit()

    def verificarVariable(self, nombre):
        if nombre in self.tabla.keys():
            pass
        else:
            print(f"Error en codigo - Variable {nombre} no definida")
            exit()

    def limpiarTabla(self):
        del (self.tabla)
        self.tabla = {}

    def imprimirTablaVariables(self):
        print("TABLA VARIABLES LOCALES: ", self.tabla)

    def agregarTraslado(self, nombre, dimension, segundaDimension=None, traslado=None):
        self.tabla[nombre][2] = dimension
        if segundaDimension:
            self.tabla[nombre].append(segundaDimension)
        if traslado:
            self.tabla[nombre].append(traslado)

    def verificarArreglo(self, nombre):
        if len(self.tabla[nombre]) >= 3:
            pass
        else:
            print(
                f"Error - Se esta tratando de indexar la variable: {nombre} como arreglo")
            quit()

    def verificarMatriz(self, nombre):
        if len(self.tabla[nombre]) == 5:
            pass
        else:
            print(
                f"Error - Se esta tratando de indexar la variable: {nombre} como matriz")
            quit()

    def esArregloMatriz(self, nombre):
        return len(self.tabla[nombre])

    def regresaDimension(self, nombre):
        return self.tabla[nombre][2]

    def regresaDimensionM(self, nombre):
        return self.tabla[nombre][2], self.tabla[nombre][3]


class Constantes:
    numeroConstantes = 2000
    dirE = 30000
    dirF = dirE + numeroConstantes
    dirT = dirF + numeroConstantes
    dirL = dirT + numeroConstantes

    def __init__(self):
        self.tablaConstantes = {}
        self.tablaConstantes["FALSO"] = self.dirL
        self.tablaConstantes["VERDADERO"] = self.dirL + 1

    def agregarConstante(self, valor, direccion, tipo):
        if tipo == 0:
            direccion = self.dirE + direccion
            if direccion >= self.dirE + self.numeroConstantes:
                print("Error - Se excedio el numero de constantes Tipo: entero")
                quit()
        elif tipo == 1:
            direccion = self.dirF + direccion
            if direccion >= self.dirF + self.numeroConstantes:
                print("Error - Se excedio el numero de constantes Tipo: flotante")
                quit()
        elif tipo == 2:
            direccion = self.dirT + direccion
            if direccion >= self.dirT + self.numeroConstantes:
                print("Error - Se excedio el numero de constantes Tipo: texto")
                quit()
        elif tipo == 3:
            direccion = self.dirL + direccion
            if direccion >= self.dirL + self.numeroConstantes:
                print("Error - Se excedio el numero de constantes Tipo: logico")
                quit()
        try:
            self.tablaConstantes[valor] = direccion
            return 0
        except:
            return -1

    def regresarDireccion(self, valor):
        return self.tablaConstantes[valor]

    def imprimir(self):
        print("\n TABLA DE CONSTANTES")
        for constante in self.tablaConstantes.keys():
            print(f"{constante} : {self.tablaConstantes[constante]}")
