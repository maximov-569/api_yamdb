from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet, CommentViewSet,
    GenreViewSet, ReviewsViewSet, TitleViewSet
)

router_v1 = DefaultRouter()
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewsViewSet, basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router_v1.urls)),
]
