from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils import timezone
from django_countries.fields import CountryField

from registration.signals import user_registered
from sorl.thumbnail import ImageField

from dj1.settings import DEFAULT_AVATAR_PATH


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    country = CountryField(null=True, blank=True)
    city = models.CharField(max_length=35, blank=True)
    bio = models.CharField(max_length=220, blank=True)
    avatar = ImageField(upload_to='img/avatar', default=DEFAULT_AVATAR_PATH)

    @property
    def location(self):
        return ', '.join(filter(None, (self.city, self.country)))

    @property
    def age(self):
        if self.birth_date:
            today = timezone.now()
            return today.year - self.birth_date.year - (
                    (today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        else:
            return None

    @staticmethod
    @receiver(user_registered)
    def create(sender, user, request, **kwargs):
        profile = Profile(user=user)
        profile.save()

    def __str__(self):
        return f'{self.user.username} profile'
