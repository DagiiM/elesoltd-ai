from django.urls import path
from . import views

urlpatterns = [
    path('documents/', views.document_landing_page, name="document"),
    path('documents/create-business-plan', views.document_create_business_plan_page, name="business_plan"),
    path('documents/create-resume-and-cover-letter', views.document_create_resume_page, name="resume"),
    path('documents/create-project-proposal', views.document_create_project_proposal_page, name="project_proposal"),
    path('documents/create-project-report', views.document_create_project_report_page, name="project_report"),
]
