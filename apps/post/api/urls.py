from django.urls import path

from .views import post_create, post_update, post_list, liked_post, comment_list, comment_create, comment_update, comment_delete

app_name = 'api_post'

urlpatterns = [

    path('list/', post_list, name='post_list'),
    path('create/', post_create, name='post_create'),
    path('update/<str:id>', post_update, name='post_update'),
    path('like/', liked_post, name='liked_post'),
    path('comment/list/', comment_list, name='comment_list'),
    path('comment/create/', comment_create, name='comment_create'),
    path('comment/update/<int:pk>/', comment_update, name='comment-update'),
    path('comment/delete/<int:pk>/', comment_delete, name='comment-delete'),
]