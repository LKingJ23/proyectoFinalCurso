from django.shortcuts import render
from hotel.models import Hotel, Habitaciones
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
# Create your views here.


def home(request):
	#Vista que carga la página principal
	habitaciones_list = Habitaciones.objects.annotate(habitaciones_count=Count('num_habitacion')).values('num_habitacion', 'habitaciones_count', 'image')
	hotel = Hotel.objects.all()
	habitaciones_count = Habitaciones.objects.count()
	template = 'home/home.html'
	context = {
		'hotel': hotel,
		'habitaciones_list': habitaciones_list,
		'habitaciones_count': habitaciones_count,
	}

	return render(request, template, context)
