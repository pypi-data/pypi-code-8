from rest_framework import serializers
from django.contrib.auth.models import User
from models import Post, UserProfile


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.HyperlinkedIdentityField(view_name='userpost-list', lookup_field='username')

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'posts', )


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False)

    def get_validation_exclusions(self, *args, **kwargs):
        # Need to exclude `user` since we'll add that later based off the request
        exclusions = super(PostSerializer, self).get_validation_exclusions(*args, **kwargs)
        return exclusions + ['author']

    class Meta:
        model = Post


class UserProfileSerializer(serializers.ModelSerializer):
    follows = UserSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
