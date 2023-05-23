from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, mixins, filters
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.users.models import User
from api_yamdb.users.permissions import Admin, Owner
from api_yamdb.users.serializers import (
    RegistrationSerializer,
    ConfirmRegistrationSerializer,
    UserSerializer,
)


@api_view(['POST'])
def registration(request):
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(User, username=serializer.validated_data['username'])
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Registration',
        f'Your confirmation code: {confirmation_code}',
        from_email='admin@yamdb.ru',
        recipient_list=[user.email]
    )
    return Response(serializer.validated_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def token_view(request):
    serializer = ConfirmRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=serializer.validated_data['username'])
    if default_token_generator.check_token(
            user, serializer.validated_data['confirmation_code']):
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserForAdminViewSet(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [Admin]
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = 'username'


class UserForOwnerViewSet(mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [Owner]
