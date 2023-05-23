from django.core.validators import EmailValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from api_yamdb.users.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """
    User registration serializer.
    """
    email = serializers.EmailField(
        max_length=254,
        required=True,
        write_only=True,
        validators=[
            EmailValidator(),
            UniqueValidator(queryset=User.objects.all())
        ],
    )
    username = serializers.CharField(
        max_length=150,
        required=True,
        write_only=True,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
    )

    class Meta:
        model = User
        fields = ('email', 'username')
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email'],
                message='Пользователь с таким username и email уже сукщетсвует!',
            )
        ]

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Нельзя использовать me как имя пользователя!')
        if value != r'^[\w.@+-]+\z':
            raise serializers.ValidationError('Неправильное имя пользователя!')
        return value


class ConfirmRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
        write_only=True,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
    )
    confirmation_code = serializers.CharField(
        required=True,
        write_only=True,
    )

    class Meta:
        model = User

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Нельзя использовать me как имя пользователя!')
        if value != r'^[\w.@+-]+\z':
            raise serializers.ValidationError('Неправильное имя пользователя!')
        return value


class UserSerializer(serializers.ModelSerializer):
    username = serializers.SlugRelatedField(
        required=True,
        slug_field='username',
        queryset=User.objects.all(),
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email'],
                message='Пользователь с таким username и email уже сукщетсвует!',
            )
        ]
