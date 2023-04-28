# Create your views here.
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import SignUpForm


def signup(request):
    """
    Vista que permite el registro de un usuario a través
    de un formulario. Crea un nuevo usario con la información
    que se le pasa en el formulario y lo guarda en la base de datos.
    Luego inicia sesión con el usuario creado y redirige a la página.
    
    :param request: Petición HTTP
    
    :return: Redirige a la página de inicio
    
    Autor: Alejandro Monterrubio
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')

    else:
        form = SignUpForm()

    context = {
        'form': form,
    }

    return render(request, 'sign_up.html', context)
