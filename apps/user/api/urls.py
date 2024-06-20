from django.urls import path

from .views import user_create

app_name = 'user_api'

urlpatterns = [
    path('create/', user_create, name='user_create')
]