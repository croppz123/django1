from django.urls import path
from . import views


app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<username>', views.profile,  name='profile'),
    path('settings/delete_avatar', views.remove_avatar, name='del_avatar'),
]
