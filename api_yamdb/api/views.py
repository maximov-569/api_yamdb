from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework import permissions, viewsets
from rest_framework.viewsets import ModelViewSet

from reviews.models import Title, Category, Genre
from .permissions import *
from .serializers import *
# Create your views here.


class TitleViewSet(ModelViewSet):
    """
    На выходе имеем набор всех произведении
    """
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    permission_classes = (Moder, Admin)
    serializer_class = (WriteTitleSerializer, ReadTitleSerializer)

    def get_serializers_class(self):
        if self.request.method in ['PATCH', 'POST', 'PUT']:
            return WriteTitleSerializer
        return ReadTitleSerializer


class GenreViewSet(ModelViewSet):
    """
    На выходе имеем набор всех жанров
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(ModelViewSet):
    """
    На выходе имеем набор всех категорий
    """
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


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
