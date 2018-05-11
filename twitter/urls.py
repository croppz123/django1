from django.urls import path
from . import views

app_name = 'twitter'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('new/', views.new, name='new'),
    path('<int:pk>/upvote', views.upvote, name='upvote'),
    path('<int:pk>/downvote', views.downvote, name='downvote'),
    path('<int:pk>/comment', views.add_comment, name='add_comment'),
    path('<int:pk>/delete', views.delete_tweet, name='delete_tweet'),
    path('tags/<tagname>', views.tags, name='tags'),

]

