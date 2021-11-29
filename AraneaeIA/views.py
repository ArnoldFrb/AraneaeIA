from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from AraneaeIA.src.core.functions import functions

global functs


def prueba(request):
    if request.POST.get('archivo'):
        return render(request, 'pages/home.html', {'uri': request.POST['archivo']})
    return render(request, 'pages/home.html')


def home(request):
    if request.method == 'POST' and request.FILES['archivo']:
        myfile = request.FILES['archivo']
        fs = FileSystemStorage()
        filename = fs.save('static/assets/utils/' + myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'pages/home.html', {'uri': uploaded_file_url})
        # functs = functions()
        # (flag, ruta_img, entradas, salidas, arañas, basesRadiales, funcionActivacion, neuronas, error) = functs.leer_datos(img)

    return render(request, 'pages/home.html', {'uri': None})


def entrenar(request):
    if request.POST.get('archivo'):
        return render(request, 'pages/home.html', {'uri': request.POST['archivo']})

    return render(request, 'pages/entrenar.html', {'uri': ''})
