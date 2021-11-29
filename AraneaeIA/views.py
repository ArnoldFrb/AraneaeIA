from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from AraneaeIA.src.core.functions import functions
from AraneaeIA.src.core.Neuron import neuron

entrenar = None
arañas = None
img = None

def prueba(request):
    if request.POST.get('archivo_simular'):
        return render(request, 'pages/home.html', {'uri': request.POST['archivo_simular']})
    return render(request, 'pages/home.html')


def home(request):
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
        (flag_data, entradas, arañas, bases_radiales, pesos) = functs.leer_datos_simulacion(uploaded_file_url)

        # SIMULACION
        simulacion = neuron(entradas, None, bases_radiales)
        (salida) = simulacion.Simulacion(pesos)

        # CARGAR PLANTILLA
        return render(request, 'pages/home.html', {'uri': salida, 'title': 'Imagen cargada'})

    return render(request, 'pages/home.html')

def entrenamiento(request):
    # CARGAR IMAGEN
    if request.method == 'POST' and request.FILES['archivo_entrenar']:
        myfile = request.FILES['archivo_entrenar']
        fs = FileSystemStorage()
        filename = fs.save('static/assets/utils/' + myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        # VARIABLESS GLOBALES
        global entrenar, arañas, img
        img = uploaded_file_url
        # LEER DATOS
        functs = functions()
        (flag_data, entradas, salidas, arañas, bases_radiales, neuronas) = functs.leer_datos(uploaded_file_url)

        entrenar = neuron(entradas, salidas, bases_radiales)
        (flag_entramiento, entrenamiento, errores) = entrenar.Entrenar()

        # CARGAR PLANTILLA
        return render(request, 'pages/entrenar.html', {'uri': entrenamiento, 'title': 'Imagen cargada'})

    return render(request, 'pages/entrenar.html')

# BUTTONS
def guardar_entranmiento(request):
    if request.method == 'POST':
        
        arañas.append([entrenar.Salidas[len(entrenar.Salidas)-1, 0], request.POST.get('title'), request.POST.get('desc'), img])
        
        functs = functions()
        functs.guardar_resultados(arañas, entrenar.Entradas, entrenar.Salidas, entrenar.BasesRadiales, entrenar.interp, len(entrenar.Entradas[0]))
        return render(request, 'pages/guardar.html', {'state': True, 'messege': 'Se guardo'})

    return render(request, 'pages/guardar.html', {'state': False, 'messege': 'No se guardo'})
