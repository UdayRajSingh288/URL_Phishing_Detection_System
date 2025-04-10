from django.urls import path
from .views import *

app_name = 'user'
urlpatterns = [
	path('', home_view, name = 'home'),
	path('signup/', signup_view, name = 'signup'),
	path('signin/', signin_view, name = 'signin')
]