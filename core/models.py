from datetime import date

from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver

from registration.signals import user_registered
from sorl.thumbnail import ImageField


class Profile(models.Model):
    DEFAULT_AVATAR = 'img/avatar/avatar_def.png'
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=35, blank=True)
    bio = models.CharField(max_length=220, blank=True)
    avatar = ImageField(upload_to='img/avatar', default=DEFAULT_AVATAR)

    @staticmethod
    @receiver(user_registered)
    def create(sender, user, request, **kwargs):
        profile = Profile(user=user)
        profile.save()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def location(self):
        return ', '.join(filter(None, (self.city, self.country)))

    def __str__(self):
        return f'{self.user.username} profile'

    @property
    def age(self):
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - \
                  ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        else:
            return 'unknown'

