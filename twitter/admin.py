from django.contrib import admin
from . import models

admin.site.register(models.Tweet)
admin.site.register(models.Vote)
admin.site.register(models.Comment)
admin.site.register(models.Tag)
