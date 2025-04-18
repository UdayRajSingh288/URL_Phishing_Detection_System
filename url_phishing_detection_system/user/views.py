from django.shortcuts import render, redirect
from .models import User
from bcrypt import hashpw, gensalt, checkpw
from requests import post
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

def check_login(request):
	e = request.COOKIES.get('email')
	p = request.COOKIES.get('password')
	if e == None or p == None:
		return False
	if len(User.objects.filter(email = e)) == 1:
		u = User.objects.get(email = e)
		if checkpw(p.encode(encoding = 'utf-8'), u.password):
			return True
		else:
			False
	else:
		return False

def home_view(request):
	if check_login(request):
		return redirect('user:detect')
	return render(request, 'user/index.html', {})

def signup_view(request):
	if check_login(request):
		return redirect('user:detect')
	if request.POST:
		e = request.POST['email']
		p = request.POST['pswd']
		if len(User.objects.filter(email = e)) == 0:
			hp = hashpw(p.encode(encoding = 'utf-8'), gensalt())
			u = User(email = e, password = hp)
			u.save()
			return redirect('user:signin')
		else:
			return render(request, 'user/message.html', {'msg': 'Email Already taken!'})
	return render(request, 'user/signup.html', {})

def signin_view(request):
	if check_login(request):
		return redirect('user:detect')
	if request.POST:
		e = request.POST['email']
		p = request.POST['pswd']
		if len(User.objects.filter(email = e)) == 1:
			u = User.objects.get(email = e)
			if checkpw(p.encode(encoding = 'utf-8'), u.password):
				response = redirect('user:detect')
				response.set_cookie('email', e)
				response.set_cookie('password', p)
				return response
			else:
				return render(request, 'user/message.html', {'msg': 'Incorrect Password!'})
		else:
			return render(request, 'user/message.html', {'msg': 'User does not exist!'})
	return render(request, 'user/signin.html', {})

def detect_view(request):
	if check_login(request) == False:
		return redirect('user:home')
	if request.POST:
		url = request.POST['url']
		resp = post('http://127.0.0.1:8080', json = {'url': url})
		return render(request, 'user/message.html', {'msg': resp.text})
	return render(request, 'user/detect.html', {})

def logout_view(request):
	if check_login(request) == False:
		return redirect('user:home')
	else:
		response = redirect('user:home')
		response.delete_cookie('email')
		response.delete_cookie('password')
		return response

def delete_view(request):
	if check_login(request) == False:
		return redirect('user:home')
	else:
		e = request.COOKIES['email']
		u = User.objects.get(email = e)
		u.delete()
		response = redirect('user:home')
		response.delete_cookie('email')
		response.delete_cookie('password')
		return response

@api_view(['POST'])
def testURL_view(request):
	e = request.data.get('email')
	p = request.data.get('password')
	l = request.data.get('url')
	if len(User.objects.filter(email = e)) == 1:
		u = User.objects.get(email = e)
		if checkpw(p.encode(encoding = 'utf-8'), u.password):
			resp = post('http://127.0.0.1:8080', json = {'url': l})
			return Response({'status': resp.text}, status=status.HTTP_200_OK)
		else:
			return Response({'status': 'PASSWORD INCORRECT!'}, status=status.HTTP_200_OK)
	else:
		Response({'status': 'USER NOT FOUND!'}, status=status.HTTP_200_OK)