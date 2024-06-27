from django.urls import path

from .views import (post_create,
                    post_update,
                    post_list,
                    liked_post,
                    comment_create,
                    post_detail)

app_name = 'api_post'

urlpatterns = [
    path('list/', post_list, name='post_list'),
    path('create/', post_create, name='post_create'),
    path('update/<str:id>', post_update, name='post_update'),
    path('detail/<str:id>', post_detail, name='post_detail'),
    path('like/', liked_post, name='liked_post'),
    path('create-comment/', comment_create, name='comment_create'),
]