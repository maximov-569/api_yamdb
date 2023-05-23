import re

from django.core.validators import EmailValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """
    User registration serializer.
    """
    username = serializers.CharField(
        max_length=150,
        required=True,
    )
    email = serializers.EmailField(
        required=True,
        max_length=254,
        validators=[
            EmailValidator(),
        ]
    )

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError("Username 'me' is not valid")
        if not re.match(r"^[\w.@+-]+$", value):
            raise serializers.ValidationError
        return value

    def validate(self, attrs):
        username = attrs['username']
        email = attrs['email']

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.email != email:
                raise serializers.ValidationError('Wrong email!')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.username != username:
                raise serializers.ValidationError('Wrong username!')

        return attrs

    class Meta:
        fields = ("username", "email")
        model = User


class ConfirmRegistrationSerializer(serializers.Serializer):
    """
    Serializer for token view.
    """
    username = serializers.CharField(
        max_length=150,
        required=True,
        write_only=True,
        allow_blank=False
    )
    confirmation_code = serializers.CharField(
        required=True,
        write_only=True,
        allow_blank=False,
        allow_null=False,
    )


class UserSerializer(serializers.ModelSerializer):
    """
    This serializer works with User model.
    """
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
    )

    def validate_username(self, value):
        if not re.match(r"^[\w.@+-]+$", value):
            raise serializers.ValidationError
        return value

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
