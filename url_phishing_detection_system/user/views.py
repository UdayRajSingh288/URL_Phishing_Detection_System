from django.shortcuts import render
from .models import User
from bcrypt import hashpw, gensalt, checkpw

def home_view(request):
	return render(request, 'user/index.html', {})

def signup_view(request):
	return render(request, 'user/signup.html', {})

def signin_view(request):
	return render(request, 'user/signin.html', {})

def signup_process_view(request):
	e = request.POST['email']
	p = request.POST['pswd']
	if len(User.objects.filter(email = e)) == 0:
		hp = hashpw(p.encode(encoding = 'utf-8'), gensalt())
		u = User(email = e, password = hp)
		u.save()
	return render(request, 'user/index.html', {})

def signin_process_view(request):
	e = request.POST['email']
	p = request.POST['pswd']
	if len(User.objects.filter(email = e)) == 1:
		u = User.objects.get(email = e)
		if checkpw(p.encode(encoding = 'utf-8'), u.password):
			print('User matched!')
		else:
			print('Incorrect Password!')
	else:
		print('User does not exist!')
	return render(request, 'user/index.html', {})