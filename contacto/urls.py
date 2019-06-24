from django.urls import path
from django.conf.urls import url
from contacto import views

app_name = 'contacto'

urlpatterns = [
    url(r'^contacto/$',views.contacto,name='contacto'),
]