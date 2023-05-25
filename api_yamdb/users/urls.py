from django.urls import path, include
from rest_framework import routers

from users.views import (
    token_view,
    UserViewSet,
    ResgisterViewSet,
)


router_v1 = routers.DefaultRouter()
router_v1.register(r'signup', ResgisterViewSet, basename='registration')
router_v1.register('', UserViewSet)

urlpatterns = [
    path('token/', token_view, name='token'),
    path('', include(router_v1.urls))
]
