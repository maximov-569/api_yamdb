from rest_framework import serializers
from reviews.models import Title, Genre, Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genre


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Category


class ReadTitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True)
    category = CategoriesSerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class WriteTitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(write_only=True, queryset=Genre.objects.all, slug_field='Slug')
    category = serializers.SlugRelatedField(write_only=True, queryset=Category.objects.all(), slug_field='slug')

    class Meta:
        fields = '__all__'
        model = Title
