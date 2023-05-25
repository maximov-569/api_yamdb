from reviews.models import Title, Category, Genre
from rest_framework.viewsets import ModelViewSet
# Create your views here.


class TitleViewSet(ModelViewSet):
    """
    На выходе имеем набор всех произведении
    """
    queryset = Title.objects.all()


class GenreViewSet(ModelViewSet):
    """
    На выходе имеем набор всех жанров
    """
    queryset = Genre.objects.all()


class CategoryViewSet(ModelViewSet):
    """
    На выходе имеем набор всех категорий
    """
    queryset = Category.objects.all()
