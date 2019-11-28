from django.db import models
from django.conf import settings

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
