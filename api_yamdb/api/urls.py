from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TitleViewSet, GenreViewSet, CategoryViewSet


router_v1 = DefaultRouter()
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('genries', GenreViewSet, basename='genries')
router_v1.register('categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('', include(router_v1.urls)),
]
