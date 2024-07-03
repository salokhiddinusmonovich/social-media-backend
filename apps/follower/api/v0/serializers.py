from rest_framework import serializers

from apps.follower.models import Follow




class FollowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['following']

class FollowingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['following', 'created_at', 'is_following']


class FollowerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['follower', 'created_at', 'is_following']

