from django.shortcuts import render


def home(request):
    return render(request, 'pages/home.html')


def prueba(request):
    if request.POST.get('archivo'):
        return render(request, 'pages/home.html', {'uri': request.POST['archivo']})


def entrenar(request):
    if request.POST.get('archivo'):
        return render(request, 'pages/home.html', {'uri': request.POST['archivo']})

    return render(request, 'pages/entrenar.html', {'uri': ''})
