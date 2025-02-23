from django.shortcuts import render, redirect
from .models import User
from random import randint
from bcrypt import hashpw, gensalt, checkpw

def index(request):
	return render(request, 'user/index.html')

def signup(request):
	return render(request, 'user/signup.html')

def signin(request):
	return render(request, 'user/signin.html')

def signup_process(request):
	try:
		email = request.POST['email']
		pswd1 = request.POST['pswd1']
		pswd2 = request.POST['pswd2']
		user = User.objects.filter(email = email)
		if user:
			return render(request, 'user/message.html', {'message': 'EMAIL ALREADY IN USE!'})
		else:
			otp = randint(1000, 9999)
			request.session['new_email'] = email
			request.session['new_pswd'] = pswd1
			request.session['otp'] = str(otp)
			print(otp)
			return render(request, 'user/otp.html')
	except:
		return render(request, 'user/message.html', {'message': 'SIGNUP ERROR!'})

def signin_process(request):
	try:
		email = request.POST['email']
		pswd = request.POST['pswd']
		message = email + ' ' + pswd
		return render(request, 'user/message.html', {'message': message})
	except:
		return render(request, 'user/message.html', {'message': 'SIGNIN ERROR!'})

def otp(request):
	try:
		otp = request.POST['otp']
		email = request.session['new_email']
		pswd = hashpw(request.session['new_pswd'].encode('utf-8'), gensalt())
		if request.session['otp'] == otp:
			user = User(email = email, password = pswd)
			user.save()
			request.session['email'] = email
			request.session['pswd'] = request.session['new_pswd']
			return redirect('url')
		else:
			return render(request, 'user/message.html', {'message': 'OTP DOES NOT MATCH!'})
	except:
		return render(request, 'user/message.html', {'message': 'OTP ERROR!'})

def url(request):
	return render(render, 'user/url.html')