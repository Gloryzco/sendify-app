from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from django.utils import timezone
from django.core.validators import MinLengthValidator, FileExtensionValidator
from django.forms import model_to_dict
from phonenumber_field.modelfields import PhoneNumberField
from .managers import UserManager
import uuid
import random
from django.contrib.auth.models import Group as DjangoGroup


class User(AbstractBaseUser, PermissionsMixin):
    
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
        ('vendor', 'Vendor'),
    )   
    
    
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    first_name    = models.CharField(_('first name'),max_length = 250)
    last_name     = models.CharField(_('last name'),max_length = 250)
    role          = models.CharField(_('role'), max_length = 255, choices=ROLE_CHOICES)
    email         = models.EmailField(_('email'), unique=True)
    phone         = PhoneNumberField(unique=True, max_length=50)
    password      = models.CharField(_('password'), max_length=300)
    is_staff      = models.BooleanField(_('staff'), default=False)
    is_admin      = models.BooleanField(_('admin'), default= False)
    is_active     = models.BooleanField(_('active'), default=True)
    is_deleted    = models.BooleanField(_('deleted'), default=False)
    date_joined   = models.DateTimeField(_('date joined'), auto_now_add=True)
    
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['id','first_name', 'last_name', 'role', 'phone', ]
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return f"{self.email} -- {self.role}"
    
    @property
    def module_access(self):
        unique_modules = ModuleAccess.objects.filter(group__user=self.id).distinct().values()
        
        return unique_modules
    
    
    def delete(self):
        self.is_deleted = True
        self.email = f"{random.randint}-deleted-{self.email}"
        self.phone = f"{self.phone}-del-{random.randint}"
        self.save()
        
        
    def delete_permanently(self):
        super().delete()
        

    
        
        
class ActivationOtp(models.Model):
    user  =models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    expiry_date = models.DateTimeField()
    
    
    def is_valid(self):
        return bool(self.expiry_date > timezone.now())


    
    
class ModuleAccess(models.Model):
    url = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    
    
    def __str__(self):
        return self.name

DjangoGroup.add_to_class('module_access', models.ManyToManyField(ModuleAccess,  blank=True))


class ActivityLog(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    
    
    def delete(self):
        self.is_deleted = True
        self.save()
        
        
    def delete_permanently(self):
        super().delete()
        
        
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} {self.action}"
    