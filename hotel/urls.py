from django.urls import path
from . import views

app_name = 'habitaciones'

urlpatterns = [
    path('', views.habitaciones_list, name='habitaciones_list'),
    path('<int:id>', views.habitacion_detail, name='habitacion_detail'),
]