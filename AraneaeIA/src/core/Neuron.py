from numpy import linalg, append, ones
from AraneaeIA.src.core.functions import functions

class neuron:

    # CONSTRUCTOR
    def __init__(self, entradas, salidas, basesRadiales):
        self.functions = functions()
        self.Entradas = entradas
        self.Salidas = salidas
        self.BasesRadiales = basesRadiales

    def Entrenar(self):
        funcion_activacion = 'BASERADIAL'
        error_maximo = 0.001

        # CALCULO DE LA DISTANCIA EUCLIDIANA
        distanciasEuclidianas = []
        for entradas in self.Entradas:
            distanciasEuclidianas.append(self.functions.DistanciaEuclidiana(entradas, self.BasesRadiales))

        # CALCULO DE LA FUNCION DE ACTIVACION
        fa = self.functions.FuncionActivacion(funcion_activacion, distanciasEuclidianas)
        
        # MATRIZ DE INTERPOLACION
        matriz = append(ones((len(fa), 1)), fa, axis=1)
        self.interp = linalg.lstsq(matriz, self.Salidas, rcond=-1)[0]
        
        # ECUACION DE BASE RADIAL
        salidas = self.functions.EcuacionBaseRadial(matriz, self.interp)
        
        # ERROR LINEAL
        (errorLineal, entrenamiento) = self.functions.ErrorLineal(self.Salidas, salidas)

        # ERROR GENERAL DEL ENTRANMIENTO
        error_general = self.functions.ErrorG(errorLineal)

        # MATRIZ DE SALIDAS YD & YR
        self.vs_errores = [error_maximo, error_general]

        return (error_general <= error_maximo, entrenamiento, self.vs_errores)

    def Simulacion(self, pesos):
        funcion_activacion = 'BASERADIAL'

        # CALCULO DE LA DISTANCIA EUCLIDIANA
        distanciasEuclidianas = []
        for entradas in self.Entradas:
            distanciasEuclidianas.append(self.functions.DistanciaEuclidiana(entradas, self.BasesRadiales))

        # CALCULO DE LA FUNCION DE ACTIVACION
        fa = self.functions.FuncionActivacion(funcion_activacion, distanciasEuclidianas)
        
        # MATRIZ DE INTERPOLACION
        matriz = append(ones((len(fa), 1)), fa, axis=1)
        
        # ECUACION DE BASE RADIAL
        salidas = self.functions.EcuacionBaseRadial(matriz, pesos)

        return salidas