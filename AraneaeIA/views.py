from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from AraneaeIA.src.core.functions import functions
from AraneaeIA.src.core.neuron import neuron

global functs
global entrenar

def home(request):
    if request.method == 'POST' and request.FILES['archivo']:
        myfile = request.FILES['archivo']
        fs = FileSystemStorage()
        filename = fs.save('static/assets/utils/' + myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        functs = functions()
        (flag_data, entradas, salidas, arañas, bases_radiales, neuronas) = functs.leer_datos(uploaded_file_url)
        
        entrenar = neuron(entradas, salidas, bases_radiales)
        (flag_entramiento, entrenamiento, errores) = entrenar.Entrenar()
        return render(request, 'pages/home.html', {'uri': bases_radiales})

        
    return render(request, 'pages/home.html', {'uri': None})

def entrenamiento(request):
    if request.POST.get('archivo'):
        return render(request, 'pages/home.html', {'uri': request.POST['archivo']})

    return render(request, 'pages/entrenar.html', {'uri': ''})

