
from skimage.io import imread
from skimage.util import crop
from math import exp, log, sqrt
import numpy as np
import pandas as pd
import os
import errno
class functions:

    # CONSTRUCTOR
    def __init__(self):
        pass

    # METODO PARA BASES RADIALES
    def generar_bases_radiales(self, min, max, row, col):
        return np.random.uniform(min, max, [row, col])

    # MEDOTO PARA OBTENER LA DISTABCIA EUCLIDIANA
    def DistanciaEuclidiana(self, entradas, matrizBasesRadiales):
        distanciasEuclidianas = []
        for basesRadiales in matrizBasesRadiales:
            sumatoria = []
            for entrada, baseRadial in zip(entradas, basesRadiales):
                sumatoria.append(pow((entrada - baseRadial), 2))
            distanciasEuclidianas.append(pow(sum(sumatoria), 0.5))
        return distanciasEuclidianas

    # METODO PARA OBTENER LA FUNCION DE ACTIVACION BASE RADIAL
    def FuncionBaseRadial(self, matrizDistanciasEuclidianas):
        funcionesActivacion = []
        for distanciasEuclidianas in matrizDistanciasEuclidianas:
            funcionActivacion = []
            for distanciaEuclidiana in distanciasEuclidianas:
                funcionActivacion.append(pow(distanciaEuclidiana, 2) * log(distanciaEuclidiana))
            funcionesActivacion.append(funcionActivacion)
        return funcionesActivacion

    # METODO PARA OBTENER LA FUNCION DE ACTIVACION GAUSSIANA
    def FuncionGaussiana(self, matrizDistanciasEuclidianas):
        funcionesActivacion = []
        for distanciasEuclidianas in matrizDistanciasEuclidianas:
            funcionActivacion = []
            for distanciaEuclidiana in distanciasEuclidianas:
                funcionActivacion.append(exp(-pow(distanciaEuclidiana, 2)))
            funcionesActivacion.append(funcionActivacion)
        return funcionesActivacion

    # METODO PARA OBTENER LA FUNCION DE ACTIVACION MULTICUADRATICA
    def FuncionMulticuadratica(self, matrizDistanciasEuclidianas):
        funcionesActivacion = []
        for distanciasEuclidianas in matrizDistanciasEuclidianas:
            funcionActivacion = []
            for distanciaEuclidiana in distanciasEuclidianas:
                funcionActivacion.append(sqrt(1 + pow(distanciaEuclidiana, 2)))
            funcionesActivacion.append(funcionActivacion)
        return funcionesActivacion

    # METODO PARA OBTENER LA FUNCION DE ACTIVACION MULTICUADRATICA INVERSA
    def FuncionMulticuadraticaInversa(self, matrizDistanciasEuclidianas):
        funcionesActivacion = []
        for distanciasEuclidianas in matrizDistanciasEuclidianas:
            funcionActivacion = []
            for distanciaEuclidiana in distanciasEuclidianas:
                funcionActivacion.append(1 / sqrt(1 + pow(distanciaEuclidiana, 2)))
            funcionesActivacion.append(funcionActivacion)
        return funcionesActivacion

    # METODO PARA CALCULAR LAS SALIDAS
    def EcuacionBaseRadial(self, funcionesActivacion, interp):
        salida = []
        for funcionActivacion in funcionesActivacion:
            sumatoria = []
            for fa, ip in zip(funcionActivacion, interp):
                sumatoria.append(fa*ip[0])
            salida.append(sum(sumatoria))
        return salida
                

    # NOMBRE DE LA FUNCION ACTIVACION
    def FuncionActivacion(self, funcionActivacion, distanciasEuclidianas):
        switcher = {
            'BASERADIAL': self.FuncionBaseRadial(distanciasEuclidianas),
            'GAUSSIANA': self.FuncionGaussiana(distanciasEuclidianas),
            'MULTICUADRATICA': self.FuncionMulticuadratica(distanciasEuclidianas),
            'MC_INVERSA': self.FuncionMulticuadraticaInversa(distanciasEuclidianas),
        }
        return switcher.get(funcionActivacion, "ERROR")

    # METODO PARA OBTENER EL ERROR LINAL
    def ErrorLineal(self, salidas, _salida):
        error = []
        entrenamiento = []
        for salida, _salida in zip(salidas, _salida):
            entrenamiento.append([salida[0], _salida])
            error.append(salida[0] - _salida)
        return (error, entrenamiento)

    # METODO PARA OBTENER EL ERROR G
    def ErrorG(self, errorLineal):
        error = 0
        for salida in errorLineal:
            error += np.abs(salida)
        return error / len(errorLineal)

    # METODO PARA LEER ARCHIVOS XLSX E INICIALIZAR LA CONFIGURACION DE LA NEURONA
    def leer_datos(self, ruta_img, ruta_arc = os.getcwd().replace(os.sep, '/')+'/AraneaeIA/src/data/Araneae.xlsx'):
        img = imread(os.getcwd().replace(os.sep, '/')+ruta_img, as_gray=True)
        if img.shape[1] < 800:
            return (False, None, None, None, None, None)
        a = img.shape[1]-800
        img = crop(img, ((0, 0), (int(a/2), a - int(a/2))), copy=False)
        array_img = np.apply_along_axis(sum, 0, img)

        entradas = []
        salidas = []

        matriz_base_radiales = None
        vs_errores = None
        neuronas = len(array_img)
        arañas = []

        if os.path.exists(ruta_arc):
            matriz = pd.read_excel(ruta_arc, sheet_name='Matriz')
            aux_salidas = np.array([[row[len(matriz.columns) - 1]] for row in matriz.to_numpy()])
            aux_entradas = np.delete(matriz.to_numpy(), len(matriz.columns) - 1, axis=1)

            for e, s in zip(aux_entradas, aux_salidas):
                entradas.append(e)
                salidas.append(s)

            if array_img in np.array(entradas):                
                return (False, None, None, None, None, None)

            entradas.append(array_img)
            salidas.append([len(salidas) + 1])

            arañas = pd.read_excel(ruta_arc, sheet_name='Araneae').to_numpy().tolist()
            vs_errores = pd.read_excel(ruta_arc, sheet_name='Errores').to_numpy().tolist()
            matriz_base_radiales = self.generar_bases_radiales(np.array(entradas).min(), np.array(entradas).max(), neuronas, len(entradas[0]))

        else:
            entradas.append(array_img)
            salidas.append([1])
            matriz_base_radiales = self.generar_bases_radiales(np.array(entradas).min(), np.array(entradas).max(), neuronas, len(entradas[0]))
            vs_errores = []
        
        return (True, np.array(entradas), np.array(salidas), arañas, matriz_base_radiales, vs_errores)

    # METODO PARA LEER ARCHIVOS XLSX E INICIALIZAR LA CONFIGURACION DE LA NEURONA
    def leer_datos_simulacion(self, ruta_img, ruta_arc = os.getcwd().replace(os.sep, '/')+'/AraneaeIA/src/data/Araneae.xlsx'):
        img = imread(os.getcwd().replace(os.sep, '/')+ruta_img, as_gray=True)
        if img.shape[1] < 800:
            return (False, None, None, None, None)
        a = img.shape[1]-800
        img = crop(img, ((0, 0), (int(a/2), a - int(a/2))), copy=False)
        array_img = np.apply_along_axis(sum, 0, img)

        pesos = None
        arañas = None
        bases_radiales = None

        if os.path.exists(ruta_arc):
            arañas = pd.read_excel(ruta_arc, sheet_name='Araneae').to_numpy().tolist()
            pesos = pd.read_excel(ruta_arc, sheet_name='Pesos').to_numpy()
            bases_radiales = pd.read_excel(ruta_arc, sheet_name='Bases Radiales').to_numpy()

            return (True, np.array([array_img]), arañas, bases_radiales, pesos)
        
        return (False, np.array([array_img]), arañas, bases_radiales, pesos)

    def guardar_resultados(self, arañas, entradas, salidas, bases_radiales, pesos, errores):
        
        df_matrix = pd.DataFrame(np.concatenate((np.array(entradas), np.array(salidas)), axis=1), columns=['X' + str(x+1) for x in range(len(entradas[0]))] + ['YD' + str(x+1) for x in range(len(salidas[0]))])
        df_arañas = pd.DataFrame(np.array(arañas), columns=['Codigo', 'title', 'desc', 'ruta'])
        df_bases_radiales = pd.DataFrame(bases_radiales, columns=['BR' + str(x+1) for x in range(len(bases_radiales[0]))])
        df_pesos = pd.DataFrame(pesos, columns=['Pesos'])
        df_errores = pd.DataFrame(np.array(errores), columns=['Error Ge.', 'Error Op.'])

        try:
            os.mkdir(os.getcwd().replace(os.sep, '/')+'/AraneaeIA/src/data')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        with pd.ExcelWriter(os.getcwd().replace(os.sep, '/')+'/AraneaeIA/src/data/Araneae.xlsx') as writer: # pylint: disable=abstract-class-instantiated
            df_matrix.to_excel(writer, sheet_name='Matriz', index=False)
            df_arañas.to_excel(writer, sheet_name='Araneae', index=False)
            df_bases_radiales.to_excel(writer, sheet_name='Bases Radiales', index=False)
            df_pesos.to_excel(writer, sheet_name='Pesos', index=False)
            df_errores.to_excel(writer, sheet_name='Errores', index=False)
            