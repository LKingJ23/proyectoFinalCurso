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
	#Función para ver todas las habitaciones
	habitaciones_list = Habitaciones.objects.all()
	reservas_habitaciones = Reservas_habitacion.objects.all()

	template = 'hotel/list.html'
	hotel = Hotel.objects.all()
	#Esta variable tiene el mismo valor que la anterior pero la he creado
	#para que cuando se cargue esta vista la pestaña de habitaciones se "ilumine"
	#en el menu de inicio
	hotel_list = Hotel.objects.all()

	address_query = request.GET.get('q')

	#En esta parte hacemos la consulta del buscador
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

	return render(request, template, context)

def habitacion_detail(request, id):
	#Función para ver en datalle la habitación seleccionada
	#Creamos las variables que recogen todas las habitaciones en base de datos, reservas,
	# y reservas de habitaciones
	habitacion_detail = Habitaciones.objects.get(num_habitacion=id)
	reserva = Reserva.objects.all()
	reservas_habitacion = Reservas_habitacion.objects.all()
	#Creamos la variable que hará que cargue dicho html
	template = 'hotel/detail.html'

	#Si la habitacion ya esta reservada aparecerá el siguiente html.	
	for reserva in reservas_habitacion:
		if habitacion_detail == reserva.reserva_habitacion:
			template = 'hotel/detail2.html'

	if request.method == 'POST':
		#Aquí recogemos los campos del formulario de la reserva de habitacion y lo tratamos
		precio = 0
		fecha_entrada = request.POST['fecha_entrada']
		fecha_entrada = datetime.datetime.strptime(fecha_entrada, '%Y-%m-%d')
		fecha_entrada = fecha_entrada.date()
		fecha_salida = request.POST['fecha_salida']
		fecha_salida = datetime.datetime.strptime(fecha_salida, '%Y-%m-%d')
		fecha_salida = fecha_salida.date()
		ocupantes = request.POST['ocupantes']
		habitacion = habitacion_detail
		reserva = datetime.date.today()
		tipo_pension = request.POST['pension']
		precio_pension = 0
		if tipo_pension == 'completa':
			precio_pension = 150.00
		elif tipo_pension == 'media':
			precio_pension = 100.00
		elif tipo_pension == 'desayuno':
			precio_pension = 60.00
		elif tipo_pension == 'nada':
			precio_pension = 0.00
		tipo_alojamiento = Tipo_alojamiento.objects.get(habitacion_tipo_alojamiento=habitacion_detail)
		if tipo_alojamiento.descripcion == 'doble':
			precio = precio_pension + 200
		elif tipo_alojamiento.descripcion == 'individual':
			precio = precio_pension + 100
		precio = precio * float(request.POST['mayor'])
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
			#Guardamos la reserva en la base de datos
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
				Precio: """ + str(precio) + """

				Encantados de poder contar contigo.
				"""

			context = ssl.create_default_context()

			with smtplib.SMTP_SSL(smtp_server, port, context = context) as server:
				server.login(sender, password)
				server.sendmail(sender, reciever, message)
			#Guardamos la reserva de habitación en la base de datos
			reserva_habitacion.save()
			return redirect('/')

	else:
		context = {
			'habitacion_detail': habitacion_detail, 
			'reservas_habitacion': reservas_habitacion,
		}

	return render(request, template, context)
