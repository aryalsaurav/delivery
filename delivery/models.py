from dataclasses import fields
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from .managers import UserBaseManager,SoftDeletionManager
# Create your models here.

class AuditFields(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True,blank=True)

    class Meta:
        abstract=True

    def delete(self,hard=False,*args,**kwargs):
        if not hard:
            self.deleted_at=timezone.now()
            super().save(*args,**kwargs)
        else:
            super().delete(*args,**kwargs)



class User(AbstractUser,AuditFields):
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
        diff = (timezone.now().date() - self.dob )
        return int(diff.days//365.25)

    def save(self,*args,**kwargs):
        if not self.username:
            self.username = self.email

        super().save(*args,**kwargs)





class DeliveryLocation(AuditFields):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)
    address = models.CharField(max_length=255,null=True,blank=True)
    primary = models.BooleanField(default=False)

    objects = SoftDeletionManager()

    def save(self,*args,**kwargs):
        if self.primary:
            prev_primary = DeliveryLocation.objects.filter(user=self.user,primary=True).exclude(id=self.id)
            for pre in prev_primary:
                pre.primary = False
                pre.save()
        super().save(*args,**kwargs)
