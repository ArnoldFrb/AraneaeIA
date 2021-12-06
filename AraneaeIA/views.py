import os
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from shutil import move
from django.core.files.storage import FileSystemStorage
from AraneaeIA.src.core.functions import functions
from AraneaeIA.src.core.neuron import neuron
from heapq import nsmallest
from numpy import array, where

entrenar = None
arañas = None
img = None
vs_errores = None


def simulacion(request):
    if request.method == 'POST' and request.FILES['archivo_simular']:
        myfile = request.FILES['archivo_simular']
        fs = FileSystemStorage()
        filename = fs.save('static/assets/utils/' + myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        # VARIABLESS GLOBALES
        global entrenar, arañas, img
        img = uploaded_file_url

        # LEER DATOS
        functs = functions()

        (flag_data, entradas, arañas, bases_radiales,
         pesos) = functs.leer_datos_simulacion(uploaded_file_url)

        if flag_data:
            # SIMULACION
            simulacion = neuron(entradas, None, bases_radiales)
            (salida) = simulacion.Simulacion(pesos)

            lista = [res[0] for res in arañas]
            res = nsmallest(1, lista, key=lambda x: abs(x-salida[0]))
            ind = lista.index(res[0])

            arañas[ind]

            # CARGAR PLANTILLA
            return JsonResponse({'title': salida[0], 'name': arañas[ind][1], 'desc': arañas[ind][2], 'uri': arañas[ind][3]})
        else:
            # CARGAR PLANTILLA
            return JsonResponse({'message': 'La imagen no cumple con los parametros de simulacion.', 'title': 'No se pudo cargar la imagen'})


def home(request):
    return render(request, 'pages/home.html')


def entrenar(request):
    # CARGAR IMAGEN
    if request.method == 'POST' and request.FILES['archivo_entrenar']:
        myfile = request.FILES['archivo_entrenar']
        fs = FileSystemStorage()
        filename = fs.save('static/assets/utils/' + myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        # VARIABLESS GLOBALES
        global entrenar, arañas, vs_errores, img
        img = uploaded_file_url

        # LEER DATOS
        functs = functions()
        (flag_data, entradas, salidas, arañas, bases_radiales, vs_errores) = functs.leer_datos(uploaded_file_url)

        if flag_data:
            entrenar = neuron(entradas, salidas, bases_radiales)
            (flag_entramiento, entrenamiento, errores) = entrenar.Entrenar()

            vs_errores.append(errores)

            nombre_aranas = list(set([i[1] for i in arañas]))

            if flag_entramiento:
                # CARGAR PLANTILLA
                return JsonResponse({'status':True,'uri': uploaded_file_url, 'entrenamiento': entrenamiento, 'errores': vs_errores, 'numero_aranas': len(nombre_aranas), 'messege': 'Entrenamiento exitoso.'})
            else:
                # CARGAR PLANTILLA
                return JsonResponse({'status':False,'messege': 'Fallo el entrenamiento', 'title': 'Error en el entrenamiento.'})
        else:
            # CARGAR PLANTILLA
            return JsonResponse({'status':False,'title': 'Error al cargar la imagen.', 'messege': 'La imagen no cumple con los parametros de simulacion o ya ha sido entrenada.'})

def ayudanos(request):
    return render(request, 'pages/entrenar.html')

# BUTTONS


def guardar_entranmiento(request):
    if request.method == 'POST':
        ruta_img = os.getcwd().replace(os.sep, '/') + img
        x = img.split("/")
        nueva_ruta = move(ruta_img, 'static/assets/images/'+x[len(x)-1])
        arañas.append([entrenar.Salidas[len(entrenar.Salidas)-1, 0],request.POST['title'], request.POST['desc'], nueva_ruta])
        functs = functions()
        functs.guardar_resultados(arañas, entrenar.Entradas, entrenar.Salidas,entrenar.BasesRadiales, entrenar.interp, vs_errores)
        return JsonResponse({'state': True, 'messege': 'Se guardo'})
    return JsonResponse({'state': False,'messege': 'No se guardo'})
