from django.urls import path

from .views import following_create, follower_create, following_list, follower_list

app_name = 'follow_api'


urlpatterns = [
    path('following-create/', following_create, name='following_create'),
    path('follower-create/', follower_create, name='follower_create'),
    path('following-list/', following_list, name='following_list'),
    path('follower-list/', follower_list, name='follower_list'),

]