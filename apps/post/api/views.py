from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import parsers, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.post.models import Post, Tag, LikedPost, Comment
from .serializers import PostCreateSerializer, PostUpdateSerializer, PostListSerializer, LikedPostSerializer, \
    CommentSerializer, CommentCreateSerializer, CommentUpdateSerializer
from .permissions import IsOwner

class PostCreateAPIView(CreateAPIView):
    serializer_class = PostCreateSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    parser_classes = (parsers.MultiPartParser, parsers.FileUploadParser, parsers.JSONParser)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


post_create = PostCreateAPIView.as_view()



class PostUpdateAPIView(UpdateAPIView):
    serializer_class = PostUpdateSerializer
    queryset = Post.objects.all()
    permission_classes = [IsOwner]

    lookup_field = 'id'

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj


post_update = PostUpdateAPIView.as_view()


class PostListAPIView(ListAPIView):
    serializer_class = PostListSerializer
    queryset = Post.objects.all()


post_list = PostListAPIView.as_view()



class LikePostAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        post_id = request.data.get('id')
        post = Post.objects.get(id=post_id)
        like = LikedPost.objects.filter(post=post,
                                     user=request.user).exists()
        if not like:
            LikedPost.objects.create(user=request.user, post=post)

            return Response({"message": "liked"})
        like.delete()
        return Response({"message": "disliked"})


liked_post = LikePostAPIView.as_view()



class CommentListAPIView(ListAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


comment_list = CommentListAPIView.as_view()


class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


comment_create =  CommentCreateAPIView.as_view()

class CommentUpdateAPIView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentUpdateSerializer
    permission_classes = (IsAuthenticated, )

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


comment_update =  CommentUpdateSerializer.as_view()


class CommentDeleteAPIView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = (IsAuthenticated, )


comment_delete =  CommentDeleteAPIView.as_view()