from django.shortcuts import render
from .models import Hotel, Habitaciones, Reserva
from .forms import ReservaForm
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
# Create your views here.


def habitaciones_list(request):
	habitaciones_list = Habitaciones.objects.all()
	print(habitaciones_list)

	template = 'hotel/list.html'
	hotel = Hotel.objects.all()
	hotel_list = Hotel.objects.all()

	address_query = request.GET.get('q')

	if address_query:
		print(address_query)
		habitaciones_list = habitaciones_list.filter(
			Q(descripcion__icontains = address_query)
		).distinct()		

	print(habitaciones_list)
	print(hotel)

	context = {
		'habitaciones_list': habitaciones_list,
		'hotel': hotel,
		'hotel_list': hotel_list
	}

	return render(request, template, context)

def habitacion_detail(request, id):
	habitacion_detail = Habitaciones.objects.get(num_habitacion=id)
	template = 'hotel/detail.html'
	
	if request.method == 'POST':
		reserva_form = ReservaForm(request.POST)
		if reserva_form.is_valid():
			reserva_form.save()
	else:
		reserva_form = ReservaForm()
	
	context = {
		'habitacion_detail': habitacion_detail, 'reserva_form': reserva_form
	}

	return render(request, template, context)
