from django.urls import path
from .views import home_view, signup_view, signin_view, signup_process_view, signin_process_view

app_name  = 'user'
urlpatterns = [
	path('', home_view, name = 'home'),
	path('signup/', signup_view, name = 'signup'),
	path('signin/', signin_view, name = 'signin'),
	path('signup_process/', signup_process_view, name = 'signup_process'),
	path('signin_process/', signin_process_view, name = 'signin_process'),
]