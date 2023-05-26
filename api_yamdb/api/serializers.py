from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        validators=[
            UniqueValidator(queryset=Genre.objects.all())
        ],
        max_length=50,
    )

    class Meta:
        fields = ('slug', 'name')
        model = Genre


class CategoriesSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        validators=[
            UniqueValidator(queryset=Category.objects.all())
        ],
        max_length=50,
    )

    class Meta:
        fields = ('name', 'slug',)
        model = Category


class ReadTitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True)
    category = CategoriesSerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class WriteTitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        write_only=True, queryset=Genre.objects.all(), slug_field='slug')
    category = serializers.SlugRelatedField(
        write_only=True, queryset=Category.objects.all(), slug_field='slug')

    class Meta:
        fields = '__all__'
        model = Title


class ReviewsSerializer(serializers.ModelSerializer):
    """Serializer for reviews."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:

        fields = '__all__'
        model = Review
        read_only_fields = ('title', )

    def validate(self, data):
        """Validate that it's not submitted by the current user."""
        title = self.context.get('title')
        request = self.context.get('request')
        if (
            request.method != 'PATCH'
            and Review.objects.filter(
                title=title, user=request.user
            ).exists()
        ):
            raise ValidationError(
                'You have already left a review for this title.'
            )
        return data

    def validate_score(self, value):
        """Validate the score value."""
        if value < 1 and value > 10:
            raise ValidationError(
                'Please rate the title from 1 to 10!')
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:

        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)
