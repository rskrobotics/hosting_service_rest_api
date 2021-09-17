from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.contrib.postgres.fields import ArrayField
from django.conf import settings
from .validators import validate_file_extension
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid
import os


def base_image_file_path(instance, filename):
    '''Generate new filepath for image'''
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('uploads/images/', filename)


def thumbnail_file_path(instance, filename):
    '''Generate new filepath for image'''
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('uploads/thumbnails/', str(filename))


class AccountPlan(models.Model):
    '''Class representing the account subscription plan'''
    name = models.CharField(max_length=15, unique=True)
    can_expire_links = models.BooleanField(default=False)
    original_link_access = models.BooleanField(default=False)
    thumbnail_sizes = ArrayField(
        models.PositiveIntegerField(), blank=True)

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        '''Creates and saves a new user'''
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        '''Creates and saves a new superuser'''
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    '''Custom user model that uses email instead of username'''
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    account_plan = models.ForeignKey(AccountPlan, on_delete=models.PROTECT,
                                     null=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.name


class BaseImage(models.Model):
    '''Model for our base image '''
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=False
    )
    name = models.CharField(max_length=50, unique=True, blank=False)
    image = models.ImageField(upload_to=base_image_file_path,
                              validators=[validate_file_extension],
                              default='default.jpg')

    def __str__(self):
        return self.name


class Thumbnail(models.Model):
    '''Thumbnails created from base image'''
    base_image = models.ForeignKey(BaseImage, on_delete=models.CASCADE,
                                   blank=False)
    thumbnail = models.ImageField(upload_to=thumbnail_file_path, blank=False)
    height = models.PositiveIntegerField(blank=False)
    name = models.CharField(default='Thumbnailname', max_length=150)

    def __str__(self):
        return self.name


class Link(models.Model):
    '''Links created for our thumbnails'''
    thumbnail = models.ForeignKey(Thumbnail, on_delete=models.CASCADE)
    access_str = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now=True)
    duration = models.PositiveIntegerField(blank=True, null=True,
                                           validators=[MinValueValidator(300),
                                                       MaxValueValidator(
                                                           30000)])

    def __str__(self):
        return self.access_str
