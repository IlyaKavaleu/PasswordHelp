from django.db import models
from django.contrib.auth.models import User


class Password_Model(models.Model):
    """Password model"""
    text = models.CharField(max_length=30)
    email_address = models.EmailField(max_length=150)
    your_password = models.CharField(max_length=25)

    def __str__(self):
        return self.text
