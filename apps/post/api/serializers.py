from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.post.models import Post, Tag, PostImage, LikedPost, Comment

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


class PostImageSerializer(serializers.ModelSerializer):
    # image = serializers.ImageField(
    #     max_length=None, allow_empty_file=False, use_url=True
    # )

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
        print(validated_data, "====")
        tags = validated_data.pop('tags')
        images = validated_data.pop('images')
        post = Post.objects.create(**validated_data)

        for tag in tags:
            tag, created = Tag.objects.get_or_create(**tag)
            post.tags.add(tag)

        for image in images:
            PostImage.objects.create(post=post, **image)

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
        serializer = LikePostSerializer(likes, many=True)
        return serializer.data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class LikePostSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = LikedPost
        fields = ['pk', 'user']


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post', 'body', 'parent']
        # extra_kwargs = {
        #
        #     'parent': {'write_only': True}
        # }

    def create(self, validated_data):
        parent = validated_data.pop('parent')
        if parent is None:
            comment = Comment.objects.create(**validated_data)
        else:
            comment = Comment.objects.create(parent=parent, **validated_data)
        return comment


class CommentParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author', 'body', 'created']

class CommentSerializer(serializers.ModelSerializer):
    parents = CommentParentSerializer(many=True, read_only=True, source='children')
    class Meta:
        model = Comment
        fields = ['id', 'author', 'body', 'created', 'parents']


class PostDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = '__all__'