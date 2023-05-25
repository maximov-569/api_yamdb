from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import TitleViewSet, GenreViewSet, CategoryViewSet


router_v1 = SimpleRouter()
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('genries', GenreViewSet, basename='genries')
router_v1.register('categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
