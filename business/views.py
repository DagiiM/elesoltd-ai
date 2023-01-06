from django.shortcuts import render

# Create your views here.

def document_landing_page(request):
    return render(request,'business/index.html')


def document_create_business_plan_page(request):
    return render(request,'business/business_plan.html')
def document_create_resume_page(request):
    return render(request,'business/resume.html')
def document_create_project_proposal_page(request):
    return render(request,'business/project_proposal.html')
def document_create_project_report_page(request):
    return render(request,'business/project_report.html')
