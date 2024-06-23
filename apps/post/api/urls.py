from django.urls import path

from .views import post_create, post_update, post_list, liked_post

app_name = 'api_post'

urlpatterns = [
    path('list/', post_list, name='post_list'),
    path('create/', post_create, name='post_create'),
    path('update/<str:id>', post_update, name='post_update'),
    path('like/', liked_post, name='liked_post'),
]