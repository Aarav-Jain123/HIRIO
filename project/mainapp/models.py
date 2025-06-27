from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    userr = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(default='-', max_length=150)
    name = models.CharField(default='', max_length=150)
    user_points = models.IntegerField(default=0)
    
    
    def __str__(self):
        return self.email