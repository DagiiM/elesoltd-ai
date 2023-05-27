from django.db import models
from authentication.models import User


class TicketCategory(models.Model):
    CATEGORY_CHOICES = (
        ('billing', 'Billing Team'),
        ('tech_support', 'Technical Support Team'),
        ('general_inquiry', 'General Inquiry Team'),
        ('feature_request', 'Feature Request Team'),
    )

    name = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general_inquiry')

    def __str__(self):
        return self.name


class TicketAssigneeGroup(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(TicketCategory, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(User, related_name='assignee_groups')

    def __str__(self):
        return self.name


class Ticket(models.Model):
    PRIORITY_CHOICES = (
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
    )

    STATUS_CHOICES = (
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_tickets')
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=1)
    category = models.ForeignKey(TicketCategory, on_delete=models.CASCADE, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} commented on "{self.ticket.title}"'


class Assignee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignee_assignments')
    group = models.ForeignKey(TicketAssigneeGroup, on_delete=models.CASCADE, related_name='group_assignees')

    def __str__(self):
        return f'{self.user} ({self.group})'
