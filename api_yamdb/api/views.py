from reviews.models import Title, Category, Genre
from .permissions import *
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from django.db.models import Avg
# Create your views here.


class TitleViewSet(ModelViewSet):
    """
    На выходе имеем набор всех произведении
    """
    queryset = Title.onjects.annotate(rating=Avg('reviews__score')).all()
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
