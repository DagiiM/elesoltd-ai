
from django.urls import path, include
from .views import AccountViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'accounts/(?P<account_pk>\d+)/cards', AccountViewSet.CardViewSet, basename='card')

urlpatterns = [
    path('', include(router.urls)),
]