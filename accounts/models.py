from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=255,unique=True)
    username = models.CharField(max_length=255,unique=True)
    # Définissez des noms de champ personnalisés pour éviter les conflits
    groups = models.ManyToManyField('auth.Group', related_name='customuser_set')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='customuser_set')
    