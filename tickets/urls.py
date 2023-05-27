from django.urls import path, include
from rest_framework import routers
from .views import TicketViewSet,TicketAssigneeViewSet


router = routers.DefaultRouter()
router.register(r'tickets', TicketViewSet)
router.register(r'ticket-assignees', TicketAssigneeViewSet)


urlpatterns = [
    path('', include(router.urls)), 
]



