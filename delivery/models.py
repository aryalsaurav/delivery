from dataclasses import fields
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from .managers import UserBaseManager
# Create your models here.


class User(AbstractUser):
    email = models.EmailField(max_length=100,unique=True,db_index=True)
    username = models.CharField(max_length=100,unique=True)
    full_name = models.CharField(max_length=100)
    dob = models.DateField()
    ph_number = models.CharField(max_length=15,db_index=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserBaseManager()

    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['ph_number']),
            models.Index(fields=['email','ph_number'])
        ]

    @property
    def age(self):
        return (timezone.now().date() - self.dob ).year

    def save(self,*args,**kwargs):
        if not self.username:
            self.username = self.email

        super().save(*args,**kwargs)





class DeliveryLocation(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)
    address = models.CharField(max_length=255,null=True,blank=True)
