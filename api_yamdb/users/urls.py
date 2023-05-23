from django.urls import path, include
from rest_framework import routers

from users.views import (
    token_view,
    UserViewSet,
    ResgisterViewSet,
)


router = routers.DefaultRouter()
router.register(r'signup', ResgisterViewSet, basename='registration')
router.register('', UserViewSet)

urlpatterns = [
    path('token/', token_view, name='token'),
    path('', include(router.urls))
]
