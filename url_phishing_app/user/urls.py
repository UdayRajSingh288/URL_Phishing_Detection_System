from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name = 'index'),
	path('signup/', views.signup, name = 'signup'),
	path('signin/', views.signin, name = 'signin'),
	path('signup_process/', views.signup_process, name = 'signup_process'),
	path('signin_process/', views.signin_process, name = 'signin_process'),
	path('otp/', views.otp, name = 'otp'),
	path('url/', views.url, name = 'url')
]