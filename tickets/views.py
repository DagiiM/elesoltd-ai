from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Ticket, Comment, Assignee
from .serializers import (
    TicketSerializer,
    TicketAssigneeSerializer,
    TicketUpdateSerializer,
    CommentSerializer,
    CreateCommentSerializer
)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def perform_create(self, serializer):
        # Automatically assign ticket to the assignee group matching its category
        category = serializer.validated_data.get('category')
        assignee = Assignee.objects.filter(group__category=category).first()
        if assignee is None:
            # No assignee found for the category, so assign to any assignee
            assignee = Assignee.objects.first()
        serializer.save(user=self.request.user, assignee=assignee.user)

    @action(detail=True, methods=['post'])
    def assign_ticket(self, request, pk=None):
        ticket = self.get_object()
        serializer = TicketAssigneeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        assignee = serializer.validated_data['assignee']
        ticket.assignee = assignee
        ticket.save()
        return Response({'status': 'Ticket assigned'})

    @action(detail=True, methods=['post'])
    def resolve_ticket(self, request, pk=None):
        ticket = self.get_object()
        serializer = TicketUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ticket.status = 'done'
        ticket.save()
        return Response({'status': 'Ticket resolved'})

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        ticket = self.get_object()
        comments = ticket.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        ticket = self.get_object()
        serializer = CreateCommentSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, ticket=ticket)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put'])
    def update_comment(self, request, pk=None):
        comment = Comment.objects.get(pk=request.data['comment_id'])
        if request.user == comment.user or request.user.is_staff:
            serializer = CreateCommentSerializer(comment, data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            comment_serializer = CommentSerializer(comment)
            return Response(comment_serializer.data)
        else:
            return Response({'detail': 'You do not have permission to perform this action.'},
                            status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['delete'])
    def delete_comment(self, request, pk=None):
        comment = Comment.objects.get(pk=request.data['comment_id'])
        if request.user == comment.user or request.user.is_staff:
            comment.delete()
            return Response({'status': 'Comment deleted.'})
        else:
            return Response({'detail': 'You do not have permission to perform this action.'},
                            status=status.HTTP_403_FORBIDDEN)


class TicketAssigneeViewSet(viewsets.ModelViewSet):
    queryset = Assignee.objects.all()
    serializer_class = TicketAssigneeSerializer
    filterset_fields = ['group__category']

    @action(detail=True, methods=['get'])
    def tickets(self, request, pk=None):
        assignee = self.get_object().user
        tickets = Ticket.objects.filter(assignee=assignee).order_by('-created_date')
        page = self.paginate_queryset(tickets)
        if page is not None:
            serializer = TicketSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
