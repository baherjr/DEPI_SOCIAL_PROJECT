from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import User, Profile, Friendship
from .serializers import UserSerializer, ProfileSerializer, FriendshipSerializer


class UserProfileView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


    def retrieve(self, request, pk=None):

        user = self.request.user
        try:
            profile = user.profile
        except Profile.DoesNotExist:
            profile = None

        user_serializer = UserSerializer(user)
        profile_serializer = ProfileSerializer(profile) if profile else None

        response_data = {
            'UserData': user_serializer.data,
            'ProfileData': profile_serializer.data if profile_serializer else None
        }

        return Response(response_data)
    
    def create(self, request):
        # Create a new user using the provided data
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        user = self.request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        user = self.request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FriendListView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        user = self.request.user
        friends = Friendship.objects.filter(user=user, friend_status='Accepted')
        friend_users = friends.values_list('friend', flat=True)
        serializer = UserSerializer(User.objects.filter(id__in=friend_users), many=True)
        return Response(serializer.data)

class FriendRequestView(viewsets.ModelViewSet):
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        user = self.request.user
        friend_requests = Friendship.objects.filter(friend=user, friend_status='Pending')
        serializer = FriendshipSerializer(friend_requests, many=True)
        return Response(serializer.data)

    def create(self, request):
        # Get the requested friend's user ID from request data
        try:
            friend_id = request.data['Fname'] + request.data["Lname"]
        except KeyError:
            return Response({'error': 'Missing friend_id in request data'}, status=status.HTTP_400_BAD_REQUEST)
    
        # Check if the friend exists
        friend = get_object_or_404(User, pk=friend_id)
    
        # Check if a friendship record already exists
        existing_friendship = Friendship.objects.filter(user=request.user, friend=friend).first()
    
        # Handle different scenarios based on existing friendship status
        if existing_friendship:
            if existing_friendship.friend_status == 'Pending':
                # Duplicate request, inform user
                return Response({'message': 'Friend request already sent'}, status=status.HTTP_409_CONFLICT)
            elif existing_friendship.friend_status == 'Accepted':
                # Already friends, inform user
                return Response({'message': 'You are already friends with this user'}, status=status.HTTP_409_CONFLICT)
            else:
                # Update existing request (e.g., blocked -> pending)
                existing_friendship.friend_status = 'Pending'
                existing_friendship.save()
                return Response({'message': 'Friend request updated'}, status=status.HTTP_200_OK)
        else:
            # Create a new friendship record with pending status
            new_friendship = Friendship.objects.create(
                user=request.user,
                friend=friend,
                friend_status='Pending'
            )
            return Response({'message': 'Friend request sent'}, status=status.HTTP_201_CREATED)
    