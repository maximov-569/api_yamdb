from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, filters, permissions, mixins
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import DEFAULT_SERVICE_ADMIN_EMAIL
from users.models import User
from users.permissions import Admin
from users.serializers import (
    RegistrationSerializer,
    ConfirmRegistrationSerializer,
    UserSerializer,
)


class ResgisterViewSet(viewsets.GenericViewSet,
                       mixins.CreateModelMixin):
    """
    ViewSet for registration.
    User send his username and email then get code for confirmation.
    """
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # If user want to get new code we except Integrity Error.
        try:
            self.perform_create(serializer)
        except IntegrityError:
            pass

        user = get_object_or_404(
            User,
            username=serializer.validated_data['username'],
        )

        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Registration',
            f'Your confirmation code: {confirmation_code}',
            from_email=DEFAULT_SERVICE_ADMIN_EMAIL,
            recipient_list=[user.email]
        )
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=headers,
        )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def token_view(request):
    """
    This view check the confirmation code and send token to user.
    """
    serializer = ConfirmRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = get_object_or_404(
        User,
        username=serializer.validated_data['username'],
    )

    if default_token_generator.check_token(
            user, serializer.validated_data['confirmation_code']):

        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    This view set allow admin to create and change user objects.
    Additional method users_profile allow user to patch and get his profile.
    """
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (Admin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    # Through this method user can get and patch it own profile.
    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        url_path="me",
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=UserSerializer,
    )
    def users_profile(self, request):
        user = request.user
        if request.method == "GET":
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == "PATCH":
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            # New role is old role
            # because user cant change the role by yourself.
            serializer.save(role=user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
