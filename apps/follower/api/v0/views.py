from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.chat.models import User
from apps.follower.models import Follow
from  .serializers import FollowingCreateSerializer, FollowerListSerializer, FollowingListSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q


class FollowingCreateAPIView(CreateAPIView):
    serializer_class = FollowingCreateSerializer
    queryset = Follow.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)

following_create = FollowingCreateAPIView.as_view()


class FollowerCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, username):
        user = User.objects.filter(username=username).first()
        follow = Follow.objects.filter(follower=user, following=self.request.user).first()
        if not follow:
            return Response({"message": "not found follow user"})
        if not follow.is_following:
            follow.is_following = True
            follow.save()
            return Response({"message": "follow back"})
        return Response({"message": "already following"})



follower_create = FollowerCreateAPIView.as_view()


class FollowingListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowingListSerializer

    def get_queryset(self):
        return Follow.objects.first(Q(following=self.request.user) | Q(is_following=True))

following_list = FollowingListAPIView.as_view()


class FollowerListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowerListSerializer

    def get_queryset(self):
        return Follow.objects.first(follower=self.request.user)


follower_list = FollowerListAPIView.as_view()