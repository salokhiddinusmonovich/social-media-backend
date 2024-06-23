from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.post.models import Post, Tag, PostImage, LikedPost

User = get_user_model()

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

class PostImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        max_length=None, allow_empty_file=False, use_url=True
    )
    class Meta:
        model = PostImage
        fields = ['image']

class PostCreateSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    images = PostImageSerializer(many=True, write_only=True)

    class Meta:
        model = Post
        fields = ['caption', 'tags', 'images']

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        images = validated_data.pop('images')
        post = Post.objects.create(**validated_data)

        for tag in tags:
            tag, created = Tag.objects.get_or_create(**tag)
            post.tags.add(tag)

        for image in images:
            PostImage.objects.create(post=post, **images)

        return post

class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['caption']

class PostListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_likes(self, obj):
        likes = LikedPost.objects.filter(post=obj)
        serializer = LikedPostSerializer(likes, many=True)
        return serializer.data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class LikedPostSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = LikedPost
        fields = ['pk', 'user']