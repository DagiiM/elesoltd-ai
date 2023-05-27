from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'document_sessions', views.DocumentSessionViewSet, basename='document_session')
router.register(r'business_plans', views.BusinessPlanViewSet, basename='business_plan')
router.register(r'resumes', views.ResumeViewSet, basename='resume')
router.register(r'project_proposals', views.ProjectProposalViewSet, basename='project_proposal')
router.register(r'project_reports', views.ProjectReportViewSet, basename='project_report')

urlpatterns = [
    path('', include(router.urls)),
    path('', views.text_processor_view, name="creator"),
    path('documents/', views.document_landing_page, name="document"),
    path('documents/create-business-plan', views.document_create_business_plan_page, name="business_plan"),
    path('documents/create-resume-and-cover-letter', views.document_create_resume_page, name="resume"),
    path('documents/create-project-proposal', views.document_create_project_proposal_page, name="project_proposal"),
    path('documents/create-project-report', views.document_create_project_report_page, name="project_report"),
]
