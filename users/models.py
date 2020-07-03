from django.db import models
from django.contrib.auth.models import AbstractUser
#Create your models here.
# class UserMedico(AbstractUser):
#     username = models.CharField(max_length=250, unique=True)
#     rut_medico=models.CharField(default="",max_length=12,blank=True, null=True, unique=True)
#     email= models.EmailField(default="",max_length=254,blank=True, null=True)
#     tipo_usuario=models.CharField(default="",max_length=50,blank=True, null=True)
#     estado=models.CharField(default="",max_length=50,blank=True, null=True)
#     USERNAME_FIELD = 'username'

class UserSistema(AbstractUser):
    username = models.CharField(max_length=250, unique=True)
    rut=models.CharField(default="",blank=True, null=True,max_length=12,unique=True)
    email= models.EmailField(max_length=254,blank=True, null=True,unique=True)
    tipo_usuario=models.CharField(default="administrador",max_length=50,blank=True, null=True)
    estado=models.BooleanField(default=True)
    USERNAME_FIELD = 'username'