from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework import viewsets, filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .mixins import ModelMixinSet
from reviews.models import Title, Category, Genre, Review, Comment

from .filters import TitleFilter
from .serializers import (
    WriteTitleSerializer,
    ReadTitleSerializer,
    GenreSerializer,
    CommentSerializer,
    ReviewsSerializer,
    CategoriesSerializer,
)
from users.permissions import ReadOnlyOrAdmin, Owner


class TitleViewSet(ModelViewSet):
    """
    На выходе имеем набор всех произведении
    """
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('id')
    permission_classes = (ReadOnlyOrAdmin,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'POST', 'PUT']:
            return WriteTitleSerializer
        return ReadTitleSerializer


class GenreViewSet(ModelMixinSet):
    """
    На выходе имеем набор всех жанров
    """
    lookup_field = 'slug'
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = (ReadOnlyOrAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(ModelMixinSet):
    """
    На выходе имеем набор всех категорий
    """
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (ReadOnlyOrAdmin,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class ReviewsViewSet(viewsets.ModelViewSet):
    """Viewset for working with reviews."""

    serializer_class = ReviewsSerializer
    permission_classes = [Owner, ]

    def get_title(self):
        """Get the title object."""
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_serializer_context(self):
        """Set up the context for serialization."""
        context = super(ReviewsViewSet, self).get_serializer_context()
        context.update({'title': self.get_title()})
        return context

    def perform_create(self, serializer):
        """Create a new review."""
        serializer.save(author=self.request.user, title=self.get_title())

    def get_queryset(self):
        """Get all reviews for the title."""
        return self.get_title().reviews.all().order_by('id')


class CommentViewSet(viewsets.ModelViewSet):
    """Viewset для работы с комментариями."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [Owner, ]

    def get_review(self):
        """Получение объекта отзыва."""
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def perform_create(self, serializer):
        """Создание нового комментария."""
        serializer.save(author=self.request.user, review=self.get_review())

    def get_queryset(self):
        """Получение всех комментариев к отзыву."""
        return self.get_review().comments.all()
