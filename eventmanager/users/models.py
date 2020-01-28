from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.dispatch import receiver
from django.db.models.signals import pre_save

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (
    BaseUserManager, 
    AbstractBaseUser, 
    PermissionsMixin
)
from core.utils import unique_slug_gen
from locations.models import Location

def upload_dir(instance, fielname):
    return "user_{0}_{1}".format(instance.id, fielname)

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
    
    location = models.OneToOneField(
        Location,
        on_delete = models.SET_NULL,
        null = True,
        related_name='user',
        related_query_name = 'user'
    )

    is_active = models.BooleanField(_('active'),default = False)
    is_volunteer = models.BooleanField(default = True)
    avatar = models.ImageField(
        upload_to = upload_dir, 
        null = True, 
        blank = True,
    )
    slug = models.SlugField()
    USERNAME_FIELD = 'email'
    REQURED_FIELDS = ['email', 'passsword',]

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

class Volunteer(models.Model):
    id = models.BigAutoField(
        primary_key=True,
        verbose_name = "ID",
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = "volunteer",
        related_query_name = "volunteer"
    )

    organizers = models.ManyToManyField(
        "Organizer",
        verbose_name = _("Organizers"),
        through =  "Subscription",
        # through_fields = ("volunteer", "organizer",),
    )

    events = models.ManyToManyField(
        "event.Event",
        verbose_name = _("Events"),
        through = "event.SavedEvent",
        # through_fields = ("volunteer", "event",),
    )

    first_name = models.CharField(
        verbose_name = _("first name"), 
        max_length=50
    )
    last_name = models.CharField(
        verbose_name = _("last name"),
        max_length=50
    )
    
    dob = models.DateField(
        verbose_name = _("date of birth"),
        null = True, 
        blank = True,
    )
    bio = models.TextField(
        verbose_name = _("biography"),
        null = True, blank = True
    )
    contact_no = models.CharField(
        null  = True,
        blank = True,
        max_length=10,
        verbose_name = _("contact no"),
        validators = [
            RegexValidator(
                regex = r'^\d{6,10}$', 
                message = "Contact number must contain digits only. Up to 10 digits allowed."
            )] 
    )

    @property
    def name(self):
        return self.__str__()
    
    def __str__(self):
        return self.first_name + " " + self.last_name

class Organizer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = "organizer",
        related_query_name = "organizer"
    )
    
    name = models.CharField(
        max_length=100,
        unique = True,
        verbose_name = _("name of organization")
    )
    description = models.TextField()


class OrganizationContact(models.Model):
    organizer = models.OneToOneField(
        Organizer,
        related_name='contact',
        related_query_name ='contact',
        on_delete = models.CASCADE,
    )
    primary_no = models.CharField(
        max_length=10,
        verbose_name = _("primary contact no"),
        validators = [RegexValidator(regex = r'^\d{6,10}$')] 
    )

    secondary_no = models.CharField(
        max_length=10,
        null = True,
        blank = True,
        verbose_name = _("secondary contact no"),
        validators = [RegexValidator(regex = r'^\d{6,10}$')] 
    )

    website = models.URLField(null = True, blank = True)
    facebook = models.URLField(null = True, blank = True)
    twitter = models.URLField(null = True, blank = True)
    instagram = models.URLField(null = True, blank = True)

@receiver(pre_save, sender = User)
def set_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_gen(instance, instance.email.split('@')[0])

class Subscription(models.Model):
    id = models.BigAutoField(
        primary_key=True,
        verbose_name = "ID",
    )

    volunteer = models.ForeignKey(
        Volunteer,
        verbose_name = _("Volunteer"),
        on_delete = models.CASCADE,
        related_name="subscriptions",
        related_query_name = "subscription"
    )

    organizer = models.ForeignKey(
        Organizer,
        verbose_name = _("Organizer"),
        on_delete = models.CASCADE,
        related_name = "subscribers",
        related_query_name = "subscriber"
    )


