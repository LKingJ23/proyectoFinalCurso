from django.contrib import admin
from .models import Hotel, Habitaciones, Tipo_pension, Precio_pension, Tipo_alojamiento, Reserva
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(Hotel)
admin.site.register(Habitaciones)
admin.site.register(Tipo_pension)
admin.site.register(Tipo_alojamiento)
admin.site.register(Reserva)

class PrecioAdmin(admin.ModelAdmin):
	list_display = ['precio', 'precio_tipo_pension', 'hotel_tipo_pension']
	search_fields = ['precio']
	list_filter = ['precio_tipo_pension']

admin.site.register(Precio_pension, PrecioAdmin)