from django.urls import path
from .views import (
    post_create,
    post_update,
    post_list,
    post_detail,
    liked_post,
    comment_create,
    liked_comment,
    comment_delete,
    post_delete,
    comment_list
)

urlpatterns = [
    path('posts/create/', post_create, name='post-create'),
    path('posts/<str:id>/', post_update, name='post-update'),
    path('posts/list/', post_list, name='post-list'),
    path('posts/delete/<str:id>/', post_delete, name='post-delete'),
    path('posts/<str:id>/', post_detail, name='post-detail'),
    path('post/like/', liked_post, name='liked-post'),
    path('comments/create/', comment_create, name='comment-create'),
    path('comments/like/', liked_comment, name='liked-comment'),
    path('comments/delete/<str:id>/', comment_delete, name='comment-delete'),
    path('comments/list/', comment_list, name='comment-list'),

]
