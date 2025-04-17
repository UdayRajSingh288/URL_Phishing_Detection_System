from django.urls import path
from .views import home_view, signup_view, signin_view, detect_view

app_name  = 'user'
urlpatterns = [
	path('', home_view, name = 'home'),
	path('signup/', signup_view, name = 'signup'),
	path('signin/', signin_view, name = 'signin'),
	path('detect/', detect_view, name = 'detect'),
]