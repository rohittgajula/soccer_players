from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.forms import ValidationError

from players.models import Player


class CustomUserManager(BaseUserManager):
  
  def get_object_by_public_id(self, public_id):
    try:
      instance = self.get(public_id=public_id)
      return instance
    except ObjectDoesNotExist:
      raise Http404("Object does not exist.")
    except (ValueError, TypeError, ValidationError):
      raise Http404("Invalid public_id")
    
  def create_user(self, email, first_name, last_name, password=None, **extra_fields):
    if email is None:
      raise ValueError("Email is required.")
    if first_name is None:
      raise ValueError("First name is required.")
    if last_name is None:
      raise ValueError("Last name is required.")
    email = self.normalize_email(email)
    user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
    user.set_password(password)
    user.is_active = True
    user.save(using=self._db)
    return user

  def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_active', True)
    extra_fields.setdefault('is_superuser', True)

    if not extra_fields.get('is_staff'):
      raise ValueError("is_staff must be true.")
    if not extra_fields.get('is_superuser'):
      raise ValueError("is_superuser must be true.")
    
    user = self.create_user(email=email, first_name=first_name, last_name=last_name, password=password, **extra_fields)
    return user


class User(AbstractBaseUser, PermissionsMixin):
  favourate_players = models.ManyToManyField(Player, related_name='fans')
  public_id = models.UUIDField(db_index=True, unique=True, editable=False, default=uuid.uuid4)
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  email = models.EmailField(db_index=True, unique=True)
  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  is_superuser = models.BooleanField(default=False)
  date_joined = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['first_name', 'last_name']

  objects = CustomUserManager()

  def __str__(self):
    return self.email