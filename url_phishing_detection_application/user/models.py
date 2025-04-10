from django.db import models

class User(models.Model):
	email = models.EmailField(primary_key = True)
	password = models.BinaryField()