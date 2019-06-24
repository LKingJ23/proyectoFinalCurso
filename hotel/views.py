from django.shortcuts import render
from .models import Hotel, Habitaciones, Reserva, Tipo_alojamiento, Tipo_pension, Precio_pension, Reservas_habitacion
from .forms import ReservaForm, TipoAlojamientoForm, TipoPensionForm, PrecioPensionForm, ReservasHabitacionForm
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User
import datetime
from django.shortcuts import redirect
import smtplib, ssl


def habitaciones_list(request):
	habitaciones_list = Habitaciones.objects.all()
	reservas_habitaciones = Reservas_habitacion.objects.all()

	template = 'hotel/list.html'
	hotel = Hotel.objects.all()
	hotel_list = Hotel.objects.all()

	address_query = request.GET.get('q')

	if address_query:
		habitaciones_list = habitaciones_list.filter(
			Q(descripcion__icontains = address_query)
		).distinct()		

	context = {
		'habitaciones_list': habitaciones_list,
		'hotel': hotel,
		'hotel_list': hotel_list,
		'reservas_habitaciones': reservas_habitaciones
	}

	#import pdb; pdb.set_trace()

	return render(request, template, context)

def habitacion_detail(request, id):
	habitacion_detail = Habitaciones.objects.get(num_habitacion=id)
	reserva = Reserva.objects.all()
	reservas_habitacion = Reservas_habitacion.objects.all()
	template = 'hotel/detail.html'
	
	for reserva in reservas_habitacion:
		if habitacion_detail == reserva.reserva_habitacion:
			template = 'hotel/detail2.html'

	if request.method == 'POST':
		fecha_entrada = request.POST['fecha_entrada']
		fecha_entrada = datetime.datetime.strptime(fecha_entrada, '%Y-%m-%d')
		fecha_entrada = fecha_entrada.date()
		fecha_salida = request.POST['fecha_salida']
		fecha_salida = datetime.datetime.strptime(fecha_salida, '%Y-%m-%d')
		fecha_salida = fecha_salida.date()
		ocupantes = request.POST['ocupantes']
		habitacion = habitacion_detail
		reserva = datetime.date.today()
		user = request.user
		if fecha_entrada > fecha_salida:
			context = {
				'habitacion_detail': habitacion_detail, 
				'reservas_habitacion': reservas_habitacion,
				'reserva': reserva,
			}
		else:
			context = {
				'habitacion_detail': habitacion_detail, 
				'reservas_habitacion': reservas_habitacion,
			}
			reserva_reserva = Reserva(reserva=user, fecha_reserva=reserva)
			reserva_reserva.save()
			reserva_reserva = Reserva.objects.latest('fecha_reserva')
			reserva_habitacion = Reservas_habitacion(
				fecha_entrada=fecha_entrada, 
				fecha_salida=fecha_salida, 
				ocupantes=ocupantes,
				reserva_habitacion=habitacion,
				reserva_reserva=reserva_reserva)
			smtp_server = 'smtp.gmail.com'
			port = 465

			sender = 'gestion.mhhoteles@gmail.com'
			password = 'Mhhoteles.1'

			reciever = user.email
			message = """\
				Enhorabuena """ + user.username + """ por su reserva.

				""" + """
				Detalles de la reserva:
				Fecha de entrada: """ + str(fecha_entrada) + """
				Fecha de salida: """ + str(fecha_salida) + """
				Ocupantes: """ + str(ocupantes) + """
				Descripcion de la habitacion: """ + str(habitacion) + """
				Fecha de la reserva: """ + str(reserva_reserva) + """

				Encantados de poder contar contigo.
				"""

			context = ssl.create_default_context()

			with smtplib.SMTP_SSL(smtp_server, port, context = context) as server:
				server.login(sender, password)
				server.sendmail(sender, reciever, message)
			reserva_habitacion.save()
			return redirect('/')

	else:
		context = {
			'habitacion_detail': habitacion_detail, 
			'reservas_habitacion': reservas_habitacion,
		}

	return render(request, template, context)
