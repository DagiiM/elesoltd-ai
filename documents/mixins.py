from rest_framework import viewsets,status
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from rest_framework.response import Response

class UserResourcesViewSet(viewsets.ModelViewSet):
    """
    Base viewset for models with a 'user' foreign key, to filter resources based on the authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        if cache.add(f'create_user_resource_lock_{self.request.user.id}', 'true', timeout=60):
            try:
                serializer.save(user=self.request.user)
            finally:
                cache.delete(f'create_user_resource_lock_{self.request.user.id}')
        else:
            # Lock is already acquired, so return an error response
            return Response({'detail': 'Another request is already creating a user resource.'}, status=status.HTTP_409_CONFLICT)
