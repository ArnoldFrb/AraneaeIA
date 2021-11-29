from django.shortcuts import render
from django.template import Template, Context


def home(request):
    if request.POST.get('archivo'):
        return render(request, 'pages/home.html', {'uri': request.POST['archivo']})

    return render(request, 'pages/home.html', {'uri': ''})


def entrenar(request):
    if request.POST.get('archivo'):
        return render(request, 'pages/home.html', {'uri': request.POST['archivo']})

    return render(request, 'pages/entrenar.html', {'uri': ''})
