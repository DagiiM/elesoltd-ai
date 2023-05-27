from django.db import models
from authentication.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .tasks import (process_business_plan,
                    process_resume, 
                    process_project_proposal,
                    process_project_report,
                    process_business_plan_pdf,
                    process_project_proposal_pdf,
                    create_resume_pdf,
                    create_project_report_pdf
                    )


class DocumentSession(models.Model):
    OPTIONS =[
        ['Business Plan','Business Plan'],
        ['Resume','Resume'],
        ['Project Proposal','Project Proposal'],
        ['Project Report','Project Report'],
    ]
    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    document_type = models.CharField(max_length=50,choices=OPTIONS)
    content = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, default='draft')
    
    def __str__(self):
        return self.document_type
    
    
class BusinessPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document_session = models.ForeignKey(DocumentSession, on_delete=models.CASCADE)
    executive_summary = models.TextField(blank=True, null=True)
    company_description = models.TextField(blank=True, null=True)
    market_analysis = models.TextField(blank=True, null=True)
    service_offered = models.TextField(blank=True, null=True)
    marketing_strategy = models.TextField(blank=True, null=True)
    swot_analysis = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, default='draft')

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document_session = models.ForeignKey(DocumentSession, on_delete=models.CASCADE)
    contact_info = models.TextField(blank=True, null=True)
    professional_summary = models.TextField(blank=True, null=True)
    work_experience = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    references = models.TextField(blank=True, null=True)
    resume = models.TextField(blank=True, null=True)
    cover_letter = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, default='draft')
    
    def __str__(self):
        return self.contact_info
    
    
class ProjectProposal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document_session = models.ForeignKey(DocumentSession, on_delete=models.CASCADE)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    objectives = models.TextField(blank=True, null=True)
    methodology = models.TextField(blank=True, null=True)
    budget = models.TextField(blank=True, null=True)
    timeline = models.TextField(blank=True, null=True)
    conclusion = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, default='draft')

    def __str__(self):
        return self.title

class ProjectReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document_session = models.ForeignKey(DocumentSession, on_delete=models.CASCADE)
    title = models.TextField(blank=True, null=True)
    literature_review = models.TextField(blank=True, null=True)
    methodology = models.TextField(blank=True, null=True)
    results = models.TextField(blank=True, null=True)
    discussion = models.TextField(blank=True, null=True)
    conclusion = models.TextField(blank=True, null=True)
    references = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, default='draft')
 
    def __str__(self):
        return self.title   
    
    
    
@receiver(post_save, sender=DocumentSession)
def handle_document_session_save(sender, instance, **kwargs):
    if instance.document_type == 'Business Plan':
        process_business_plan(instance)
    elif instance.document_type == 'Resume':
        process_resume(instance)
    elif instance.document_type == 'Project Proposal':
        process_project_proposal(instance)
    elif instance.document_type == 'Project Report':
        process_project_report(instance)

@receiver(post_save, sender=DocumentSession)
def handle_document_session_delete(sender, instance, **kwargs):
    # Perform operations for all document types, if any
    pass    

@receiver(post_save, sender=BusinessPlan)
def create_project_proposal(sender, instance, **kwargs):
    process_business_plan_pdf(instance)
    
@receiver(post_save, sender=ProjectProposal)
def create_project_proposal(sender, instance, **kwargs):
    process_project_proposal_pdf(instance)

@receiver(post_save, sender=Resume)
def create_resume(sender, instance, **kwargs):
    create_resume_pdf(instance)

@receiver(post_save, sender=ProjectReport)
def create_project_report(sender, instance, **kwargs):
    create_project_report_pdf(instance)