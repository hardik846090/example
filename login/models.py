from django.db import models


# Create your models here.

class Login(models.Model):
    email = models.CharField(max_length=50)
    mobile = models.CharField(max_length=13)
    password = models.CharField(max_length=12, null=True)
    role = models.CharField(max_length=10)
    createdAt = models.DateField(auto_now_add=True)
    loginStatus = models.CharField(max_length=12)
    authantication = models.CharField(max_length=500, null=True)
