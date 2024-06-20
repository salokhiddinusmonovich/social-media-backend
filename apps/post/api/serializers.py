from rest_framework import serializers
from apps.post.models import Post
from django.contrib.auth.models import User


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author")