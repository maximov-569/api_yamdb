from django.urls import path, include
from rest_framework import routers

from api_yamdb.users.views import (
    token_view,
    registration,
    UserForAdminViewSet,
    UserForOwnerViewSet,
)

router = routers.DefaultRouter()
router.register('', UserForAdminViewSet)
router.register('me', UserForOwnerViewSet)

urlpatterns = [
    path('token/', token_view(), name='token_obtain'),
    path('signup/', registration(), name='registration'),
    path('', include(router.urls))
]
