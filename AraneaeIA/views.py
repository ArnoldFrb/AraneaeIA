from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from AraneaeIA.src.core.functions import functions
from AraneaeIA.src.core.neuron import neuron

functs = None
entrenar = None

def prueba(request):
    if request.POST.get('archivo'):
        return render(request, 'pages/home.html', {'uri': request.POST['archivo']})
    return render(request, 'pages/home.html')


def home(request):
    # CARGAR IMAGEN
    if request.method == 'POST' and request.FILES['archivo']:
        myfile = request.FILES['archivo']
        fs = FileSystemStorage()
        filename = fs.save('static/assets/utils/' + myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        # LEER DATOS
        global functs
        functs = functions()
        (flag_data, entradas, salidas, arañas, bases_radiales, neuronas) = functs.leer_datos(uploaded_file_url)
        
        # REALIZAR ENTRENAMIENTO
        global entrenar
        entrenar = neuron(entradas, salidas, bases_radiales)
        (flag_entramiento, entrenamiento, errores) = entrenar.Entrenar()

        # CARGAR PLANTILLA
        return render(request, 'pages/home.html', {'uri': entrenamiento})

        
    return render(request, 'pages/home.html', {'uri': None})

def entrenamiento(request):
    if request.POST.get('archivo'):
        return render(request, 'pages/home.html', {'uri': request.POST['archivo']})

    return render(request, 'pages/entrenar.html', {'uri': ''})

# BUTTONS

def guardar_entranmiento():
    print(entrenar.entradas)
