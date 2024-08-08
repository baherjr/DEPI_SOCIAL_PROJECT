from rest_framework import serializers
from .models import User, Profile, Friendship

class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    friendships = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_profile(self, obj):
        try:
            profile = obj.profile
            return ProfileSerializer(profile).data
        except Profile.DoesNotExist:
            return None

    def get_friendships(self, obj):
        friendships = obj.friendship_set.all()
        return FriendshipSerializer(friendships, many=True).data

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('Fname', 'Lname', 'bio', 'location')

class FriendshipSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    friend = serializers.SerializerMethodField()

    class Meta:
        model = Friendship
        fields = ('friend_status', 'user', 'friend')

    def get_user(self, obj):
        return UserSerializer(obj.user).data

    def get_friend(self, obj):
        return UserSerializer(obj.friend).data
