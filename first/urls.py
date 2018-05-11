from django.urls import path
from . import views


app_name = 'first'

urlpatterns = [
    path('archive/<int:year>/', views.year_archive, name='year_archive'),
    path('archive/<int:year>/<int:month>/', views.month_archive, name='month_archive'),
    path('<int:pk>/', views.article_detail, name='detail'),
]
