from django import forms
from .models import Hotel, Habitaciones, Reserva


class ReservaForm(forms.ModelForm):
	class Meta:
		model = Reserva
		fields = 'fecha_reserva',
