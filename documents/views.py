from .models import (
    DocumentSession,
    BusinessPlan,
    Resume,
    ProjectProposal,
    ProjectReport,
)
from .serializers import (
    DocumentSessionSerializer,
    BusinessPlanSerializer,
    ResumeSerializer,
    ProjectProposalSerializer,
    ProjectReportSerializer,
)
from .mixins import UserResourcesViewSet
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import os
from . chat import generate_text

class DocumentSessionViewSet(UserResourcesViewSet):
    """
    Viewset for DocumentSession model.
    """

    queryset = DocumentSession.objects.all()
    serializer_class = DocumentSessionSerializer


class BusinessPlanViewSet(UserResourcesViewSet):
    """
    Viewset for BusinessPlan model.
    """

    queryset = BusinessPlan.objects.all()
    serializer_class = BusinessPlanSerializer


class ResumeViewSet(UserResourcesViewSet):
    """
    Viewset for Resume model.
    """

    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer


class ProjectProposalViewSet(UserResourcesViewSet):
    """
    Viewset for ProjectProposal model.
    """

    queryset = ProjectProposal.objects.all()
    serializer_class = ProjectProposalSerializer


class ProjectReportViewSet(UserResourcesViewSet):
    """
    Viewset for ProjectReport model.
    """

    queryset = ProjectReport.objects.all()
    serializer_class = ProjectReportSerializer



def text_processor_view(request):
    input_text = request.POST.get('message')
    if input_text is not None:
        # Generate Text
        response = generate_text(input_text)
        data = {'response': response}
        #data = parse.process_text(response)
        return JsonResponse(data)
    else:
        return render(request,"form/text-processor.html")
    

   
   
def document_landing_page(request):
    return render(request,'form/index.html')

def document_create_business_plan_page(request):
    return render(request,'form/business_plan.html')

def document_create_resume_page(request):
    return render(request,'form/resume.html')  

def document_create_project_proposal_page(request):
    return render(request,'form/project_proposal.html')

def document_create_project_report_page(request):
    return render(request,'form/project_report.html')