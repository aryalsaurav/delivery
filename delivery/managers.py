from django.contrib.auth.models import BaseUserManager
from datetime import datetime
from django.db import models


class UserBaseManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError('Email is required to create user')
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('dob',datetime.now())
        return self.create_user(email,password,**extra_fields)


    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)

    def get_deleted(self):
        return super().get_queryset().filter(deleted_at__isnull=False)



class SoftDeletionManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)

    def get_deleted(self):
        return super().get_queryset().filter(deleted_at__isnull=False)
