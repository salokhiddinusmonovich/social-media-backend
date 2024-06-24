from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.post.models import Post, Tag, PostImage, LikedPost, Comment

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


class CommentSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(source="post.id", read_only=True)
    author_username = serializers.CharField(source="author.username", read_only=True)
    commented_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "author_username", "post_id", "body", "commented_at")

class CommentCreateSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Comment
        fields = ['post_id', 'body']

    def create(self, validated_data):
        post_id = validated_data.pop('post_id')
        post = Post.objects.get(id=post_id)
        comment = Comment.objects.create(post=post, **validated_data)
        return comment


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['body']
