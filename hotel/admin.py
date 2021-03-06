from django.contrib import admin
from .models import Hotel, Habitaciones, Tipo_pension, Precio_pension, Tipo_alojamiento, Reserva, Valoraciones, Reservas_habitacion
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(Hotel)
admin.site.register(Habitaciones)
admin.site.register(Tipo_pension)
admin.site.register(Tipo_alojamiento)
admin.site.register(Reserva)
admin.site.register(Valoraciones)

class PrecioAdmin(admin.ModelAdmin):
	list_display = ['precio', 'precio_tipo_pension', 'hotel_tipo_pension']
	search_fields = ['precio']
	list_filter = ['precio_tipo_pension']

class ReservaHabitacionAdmin(admin.ModelAdmin):
	list_display = ['fecha_entrada', 'fecha_salida', 'ocupantes', 'reserva_reserva']
	search_fields = ['fecha_entrada', 'fecha_salida']
	list_filter = ['fecha_entrada']
	

admin.site.register(Precio_pension, PrecioAdmin)
admin.site.register(Reservas_habitacion, ReservaHabitacionAdmin)