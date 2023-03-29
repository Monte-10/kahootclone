from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    
    groups = None
    user_permissions = None
    
    USERNAME_FIELD = 'username'
    
    def __str__(self):
        return self.username
