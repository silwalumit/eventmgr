from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _

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
        blank = True,
        null = True
    )
    is_active = models.BooleanField(_('active'),default = False)
    # avatar = models.ImageField(upload_to = 'avatars', null = True, blank = True)
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
