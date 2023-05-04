import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from rest_framework import generics

class UserManager(BaseUserManager):
    use_in_migrations =  True

    def _default_create(self, email, password, sex, inn, **extra_fields):
        if not email:
            raise ValueError('The email field must be set')
        user = self.normalize_email(email)
        user = self.model(email=email, sex=sex, inn=inn, **extra_fields)
        user.set_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password, sex = None, inn = None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', False)
        return self._default_create(email, password, sex, inn, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('sex', 'f')
        extra_fields.setdefault('inn', '987654321')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self._default_create(email, password, **extra_fields)



class User(AbstractUser):
    sex = (
        ('m', 'male'),
        ('f', 'female'),
    )

    username = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField('email address', unique=True)
    password = models.CharField(max_length=100)
    sex = models.CharField(max_length=6, choices=sex)
    inn = models.CharField(max_length=15, unique=True) 
    activation_code = models.CharField(max_length=36, blank=True)
    users_reset_code = models.CharField(max_length=36, blank=True)
    is_active = models.BooleanField('active field', default=False)
    

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    def create_activation_code(self):
        code = str(uuid.uuid4())
        self.activation_code = code

    def activate_with_code(self, code):
        if str(self.activation_code) != str(code):
            raise Exception("Code doesn't match")
        else:
            self.activation_code = ''
            self.is_active = True
            self.save(update_fields=['is_active', 'activation_code'])