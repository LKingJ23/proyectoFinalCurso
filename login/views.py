from django.shortcuts import render
#from login.forms import UserForm,UserProfileInfoForm, TrainBotForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import UserForm
import smtplib, ssl


def home(request):
    return render(request,'login/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in !")

@login_required
def user_logout(request):
    logout(request)
    return redirect('/')

def register(request):
    #Vista que carga la página de registro
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            #Guarda el usuario y manda un email al usuario dando la bienvenida
            user.save()
            smtp_server = 'smtp.gmail.com'
            port = 465

            sender = 'gestion.mhhoteles@gmail.com'
            password = 'Mhhoteles.1'

            reciever = user.email
            message = """\
            Bienvenido a MH Hoteles """ + user.username + """

            Encantados de poder contar contigo entre nuestros clientes.
            """

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL(smtp_server, port, context = context) as server:
                server.login(sender, password)
                server.sendmail(sender, reciever, message)
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request,'login/registration.html',
                          {'user_form':user_form,
                           'registered':registered})

def user_login(request):
    #Vista que carga el login
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return redirect('/')
            else:
                return HttpResponse("Tu cuenta esta inactiva.")
        else:
            print("Alguien intento iniciar sesión y falló.")
            print("Nombre: {} y contraseña: {}".format(username,password))
            return HttpResponse("Login incorrecto")
    else:
        return render(request, 'login/login.html', {})
