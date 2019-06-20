from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Hotel(models.Model):
	nombre = models.CharField(max_length=50)
	ubicacion = models.CharField(max_length=50)
	ciudad = models.CharField(max_length=50)
	estrellas = models.IntegerField(default=0)
	image = models.ImageField(upload_to='hotel/')

	def __str__(self):
		return self.nombre

	class Meta:
		verbose_name = 'Hotel'
		verbose_name_plural = 'Hoteles'

class Tipo_pension(models.Model):
	tipo_pension = models.CharField(max_length=50)

	def __str__(self):
		return self.tipo_pension

	class Meta:
		verbose_name = 'Tipo Pension'
		verbose_name_plural = 'Tipo Pensiones'

class Precio_pension(models.Model):
	precio = models.DecimalField(max_digits=5, decimal_places=2)
	precio_tipo_pension = models.ForeignKey('Tipo_pension', on_delete=models.CASCADE)
	hotel_tipo_pension = models.ForeignKey('Hotel', on_delete=models.CASCADE)

	def __str__(self):
		return str(self.precio)

	class Meta:
		verbose_name = 'Precio Pension'
		verbose_name_plural = 'Precio Pensiones'

class Habitaciones(models.Model):
	descripcion = models.CharField(max_length=150)
	image = models.ImageField(upload_to='habitaciones/')
	num_habitacion = models.IntegerField(default=0)
	baños = models.IntegerField(default=0)
	garaje = models.IntegerField(default=0)
	camas = models.IntegerField(default=0)
	habitacion_hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE)

	def __str__(self):
		return self.descripcion

	class Meta:
		verbose_name = 'Habitacion'
		verbose_name_plural = 'Habitaciones'

class Tipo_alojamiento(models.Model):
	descripcion = models.CharField(max_length=50)
	precio = models.DecimalField(max_digits=5, decimal_places=2)
	habitacion_tipo_alojamiento = models.ForeignKey('Habitaciones', on_delete=models.CASCADE)

	def __str__(self):
		return self.descripcion

	class Meta:
		verbose_name = 'Tipo Alojamiento'
		verbose_name_plural = 'Tipos Alojamientos'

class Reserva(models.Model):
	reserva = models.ForeignKey(User, on_delete=models.CASCADE)
	fecha_reserva = models.DateField()
