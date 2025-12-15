from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserProfileSerializer
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user)
        return Response({
            'token': token.key,
            'username': user.username
        })


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, user_id):
    try:
        target_user = User.objects.get(id=user_id)

        if target_user == request.user:
            return Response(
                {"error": "You cannot follow yourself"},
                status=status.HTTP_400_BAD_REQUEST
            )

        request.user.following.add(target_user)
        return Response(
            {"message": f"You are now following {target_user.username}"},
            status=status.HTTP_200_OK
        )

    except User.DoesNotExist:
        return Response(
            {"error": "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request, user_id):
    try:
        target_user = User.objects.get(id=user_id)
        request.user.following.remove(target_user)

        return Response(
            {"message": f"You unfollowed {target_user.username}"},
            status=status.HTTP_200_OK
        )

    except User.DoesNotExist:
        return Response(
            {"error": "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )
