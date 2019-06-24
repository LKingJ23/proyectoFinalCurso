from django.shortcuts import render
import smtplib, ssl
from django.shortcuts import redirect

def contacto(request):
	template = 'contacto/contacto.html'

	if request.method == 'POST':
		nombre = request.POST['fname']
		apellidos = request.POST['lname']
		email = request.POST['email']
		mensaje = request.POST['message']
		smtp_server = 'smtp.gmail.com'
		port = 465

		sender = 'gestion.mhhoteles@gmail.com'
		password = 'Mhhoteles.1'

		reciever = 'LKingJ23@gmail.com'
		message = """\
			Gestion de MH Hoteles 

			El cliente """ + nombre + """ """+ apellidos + """ con el email """ + email + """ envio el mensaje: 
			""" + mensaje

		context = ssl.create_default_context()

		with smtplib.SMTP_SSL(smtp_server, port, context = context) as server:
			server.login(sender, password)
			server.sendmail(sender, reciever, message)
		return redirect('/')

	return render(request, template)