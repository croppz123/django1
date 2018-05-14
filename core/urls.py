from django.urls import path
from . import views


app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.my_profile,  name='my_profile'),
    path('profile/<username>/', views.profile,  name='profile'),
    path('settings/profile/', views.profile_edition, name='profile_edition'),
    path('settings/delete_avatar/', views.remove_avatar, name='del_avatar'),
]
