from django.db import models
from django.conf import settings
from django.core.mail import send_mail

from django.dispatch import receiver
from django.db.models.signals import pre_save

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (
    BaseUserManager, 
    AbstractBaseUser, 
    PermissionsMixin
)
from core.utils import unique_slug_gen

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email,password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address.')

        user = self.model(
            email = self.normalize_email(email), 
            **extra_fields
        )

        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name = _('email address'),
        max_length = 255,
        unique = True,
    )
    username = models.CharField(
        verbose_name = _('user name'),
        max_length = 255,
    )
    is_active = models.BooleanField(_('active'),default = False)
    # avatar = models.ImageField(upload_to = 'avatars', null = True, blank = True)
    slug = models.SlugField()
    USERNAME_FIELD = 'email'
    REQURED_FIELDS = ['username', 'email', 'passsword',]

    @property
    def is_staff(self):
        if self.is_superuser:
            return True

    objects = UserManager()
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def email_user(self, subject, message, from_email = None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

@receiver(pre_save, sender = User)
def set_slug(sender, instance, **kwargs):
    instance.slug = unique_slug_gen(instance, instance.email)

class Volunteer(models.Model):
    MALE = "M"
    FEMALE = "F"
    OTHERS = "O"

    SEX_CHOICES = (
        (MALE, "Male"),
        (FEMALE, "Female"),
        (OTHERS, "Others")
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(
        max_length=50, 
        null = True, 
        blank = True
    )
    gender = models.CharField(
        max_length=1,
        choices=SEX_CHOICES
    )
    @property
    def name(self):
        return self.__str__()
    
    def __str__(self):
        if self.middle_name:
            return self.first_name + " " + self.middle_name\
             + " " + self.last_name
        return self.first_name + " " + self.last_name

    def get_absolute_url(self):
        pass

class Organization(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
    )
    name = models.CharField(
        max_length=100,
        unique = True,
        verbose_name = _("name of organization")
    )
    def get_absolute_url(self):
        pass
