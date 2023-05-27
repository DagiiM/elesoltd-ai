from django.contrib import admin
from .models import Ticket, TicketCategory, TicketAssigneeGroup, Comment, Assignee

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'assignee', 'status', 'priority', 'category', 'created_date', 'updated_date')
    list_filter = ('status', 'priority', 'category')
    search_fields = ('title', 'user__username', 'assignee__username')
    readonly_fields = ['user', 'title','description']

@admin.register(TicketCategory)
class TicketCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(TicketAssigneeGroup)
class TicketAssigneeGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    filter_horizontal = ('assignees',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'user', 'created_date')

@admin.register(Assignee)
class AssigneeAdmin(admin.ModelAdmin):
    list_display = ('user', 'group')
    list_filter = ('group', 'user__is_active')
