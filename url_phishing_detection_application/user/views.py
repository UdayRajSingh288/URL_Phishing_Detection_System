from django.shortcuts import render
from .forms import UserForm


def home_view(request):
	return render(request, 'user/index.html', {})

def signup_view(request):
	return render(request, 'user/signup.html', {})

def signin_view(request):
	return render(request, 'user/signup.html', {})