from rest_framework import serializers
from .models import Ticket, Assignee, Comment
from authentication.models import User

class TicketSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    assignee_username = serializers.ReadOnlyField(source='assignee.username')
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Ticket
        fields = ['id', 'user', 'user_username', 'assignee_username', 'title', 'description', 'status', 'priority', 'category', 'category_name', 'created_date', 'updated_date']


class TicketAssigneeSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='group.category.name')
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Assignee
        fields = ['id', 'user', 'user_username', 'group', 'category_name']


class TicketUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'status', 'assignee']

class CommentSerializer(serializers.ModelSerializer):
    ticket_id = serializers.ReadOnlyField(source='ticket.id')
    user_username = serializers.ReadOnlyField(source='user.username')
    assignee_username = serializers.ReadOnlyField(source='assignee.username')

    class Meta:
        model = Comment
        fields = ['id', 'ticket_id', 'user', 'user_username', 'text', 'created_date', 'assignee_username']

class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text']
