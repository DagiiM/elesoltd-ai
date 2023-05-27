from django.contrib import admin
from .models import (DocumentSession,
                     BusinessPlan, 
                     Resume,
                     ProjectProposal,
                     ProjectReport
                     )

@admin.register(DocumentSession)
class DocumentSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'document_type', 'created_at', 'status')
    list_filter = ('document_type', 'created_at', 'status')
    search_fields = ('user__username', 'document_type')

@admin.register(BusinessPlan)
class BusinessPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'document_session', 'status')
    list_filter = ('user', 'document_session', 'status')
    search_fields = ('user__username', 'document_session__document_type')

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('user', 'document_session', 'status')
    list_filter = ('user', 'document_session', 'status')
    search_fields = ('user__username', 'document_session__document_type')

@admin.register(ProjectProposal)
class ProjectProposalAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'status')
    list_filter = ('user', 'document_session', 'status')
    search_fields = ('user__username', 'document_session__document_type')

@admin.register(ProjectReport)
class ProjectReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'document_session', 'title', 'status')
    list_filter = ('user', 'document_session', 'status')
    search_fields = ('user__username', 'document_session__document_type')
