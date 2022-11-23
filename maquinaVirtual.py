from directorio import Directorio
from directorio import Constantes


class MaquinaVirtual:
    cuadruplos = []
    migajas = []
    codigosOperaciones = {
        'GOTO MAIN' : 0,
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
        'VERIFICADIM' : 15,
        '+DIR' : 16,
        '<':17,
        '>':18,
        '<>':19,
        '==':20,
        '||':21,
        '&&':22
    }
    directorioFunciones = Directorio()
    tablaConstantes = Constantes()

    def __init__(self, cuadruplos, directorio, tablaConstantes):
        self.cuadruplos = cuadruplos
        self.directorioFunciones = directorio
        self.tablaConstantes = tablaConstantes
        self.inicializarCuadruplos()

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

    def debug(self,indice):
        print(f"Corriendo cuaduplo: {indice}")

    def ejecucion(self):
        pila = self.cuadruplos.pilaCuadruplos
        indice = 1
        while indice <= len(pila):
            cuadruplo = pila[indice]
            self.debug(indice)
            print(cuadruplo)

            if cuadruplo[0] == 0:  #GOTOMAIN
                indice = cuadruplo[-1]
                print(indice)


            elif cuadruplo[0] == 1: #ASIGNACION
                indice += 1

            elif cuadruplo[0] == 2: #SUMA
                op1 = cuadruplo[1]
                #OBTENER EL VALOR ACTUAL DE OP1
                op2 = cuadruplo[2] 
                #OBTENER EL VALOR ACTUAL DE OP2

                resultado = op1 + op2
                #Guardar resultado en tabla 
                #tabla[cuadruplo[3]] = resultado
                indice += 1

            elif cuadruplo[0] == 3: #RESTA
                op1 = cuadruplo[1]
                #OBTENER EL VALOR ACTUAL DE OP1
                op2 = cuadruplo[2] 
                #OBTENER EL VALOR ACTUAL DE OP2

                resultado = op1 - op2
                #Guardar resultado en tabla 
                #tabla[cuadruplo[3]] = resultado
                indice += 1

            elif cuadruplo[0] == 4: #Multiplicacion
                op1 = cuadruplo[1]
                #OBTENER EL VALOR ACTUAL DE OP1
                op2 = cuadruplo[2] 
                #OBTENER EL VALOR ACTUAL DE OP2

                resultado = op1 * op2
                #Guardar resultado en tabla 
                #tabla[cuadruplo[3]] = resultado
                indice += 1

            elif cuadruplo[0] == 5: #DIVISION
                op1 = cuadruplo[1]
                #OBTENER EL VALOR ACTUAL DE OP1
                op2 = cuadruplo[2] 
                #OBTENER EL VALOR ACTUAL DE OP2

                resultado = op1 / op2
                #Guardar resultado en tabla 
                #tabla[cuadruplo[3]] = resultado
                indice += 1

            elif cuadruplo[0] == 6: #ENDFUNC
                indice = self.migajas.pop()

            elif cuadruplo[0] == 7: #ERA
                #CARGAR MEMORIA LOCAL
                indice += 1

            elif cuadruplo[0] == 8: #PARAMETER

                indice += 1

            elif cuadruplo[0] == 9: #GOSUB
                indice += 1

            elif cuadruplo[0] == 10: #IMPRIME
                direccion = cuadruplo[-1]
                valor = 0#BUSCAR EN TABLA
                print(valor)
                indice += 1

            elif cuadruplo[0] == 11: #LEER
                variable = "a" #OBTENER NOMBRE DE VARIABLE
                valor = input(f"Ingresa el valor de {variable}: ")
                #UPDATE AL VALOR EN TABLA
                indice += 1

            elif cuadruplo[0] == 12: #GOTOF
                #if !cuadruplo[1].obtenerValor:
                    #indice = curadruplo[-1]
                #else:
                    #indice += 1

                indice = cuadruplo[-1] #ELIMINAR

            elif cuadruplo[0] == 13: #GOTO
                indice = cuadruplo[-1]

            elif cuadruplo[0] == 14: #GOTOT
                #if cuadruplo[1].obtenerValor:
                    #indice = cuadruplo[-1]
                #else:
                    #indice += 1
                indice +=1 #ELIMINAR
            
            elif cuadruplo[0] == 15: #VERIFICADIM
                index = cuadruplo[1]
                limInf = cuadruplo[2]
                limSup = cuadruplo[3]
                if index <= limSup and index >= limInf:
                    indice += 1
                else:
                    print("Error en Ejecucion- Indice fuera de dimensiones")
                    quit()
                
            
            elif cuadruplo[0] == 16: # +DIR
                indice += 1
                
            elif cuadruplo[0] == 17: # <
                op1 = cuadruplo[1]
                op2 = cuadruplo[2]
                res = op1 < op2 
                #actualizar valor
                indice += 1
                
            elif cuadruplo[0] == 18: # >
                op1 = cuadruplo[1]
                op2 = cuadruplo[2]
                res = op1 > op2 
                #actualizar valor
                indice += 1
                
            elif cuadruplo[0] == 19: # <>
                op1 = cuadruplo[1]
                op2 = cuadruplo[2]
                res = op1 != op2 
                #actualizar valor
                indice += 1
                
            elif cuadruplo[0] == 20: # ==
                op1 = cuadruplo[1]
                op2 = cuadruplo[2]
                res = op1 == op2 
                #actualizar valor
                indice += 1
                
            elif cuadruplo[0] == 21: # ||
                op1 = cuadruplo[1]
                op2 = cuadruplo[2]
                res = op1  or op2 
                #actualizar valor
                indice += 1
                
            elif cuadruplo[0] == 22: # &&
                op1 = cuadruplo[1]
                op2 = cuadruplo[2]
                res = op1 and op2 
                #actualizar valor
                indice += 1
            else :
                print("CICLOOOOO")
                quit()
                
