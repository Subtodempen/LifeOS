from django.db import models

class UserAccount(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    
    credits = models.IntegerField()
