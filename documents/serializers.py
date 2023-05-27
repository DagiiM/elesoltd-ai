from rest_framework import serializers
from .models import (
    DocumentSession,
    BusinessPlan,
    Resume,
    ProjectProposal,
    ProjectReport,
)
from authentication.serializers import UserSerializer


class DocumentSessionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = DocumentSession
        fields = ["id", "user", "document_type", "content",'status','created_at']
        

class BusinessPlanSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    document_session = DocumentSessionSerializer(read_only=True)

    class Meta:
        model = BusinessPlan
        fields = [
            "id",
            "user",
            "document_session",
            "executive_summary",
            "company_description",
            "market_analysis",
            "service_offered",
            "marketing_strategy",
            "management_team",
        ]


class ResumeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    document_session = DocumentSessionSerializer(read_only=True)

    class Meta:
        model = Resume
        fields = [
            "id",
            "user",
            "document_session",
            "contact_info",
            "professional_summary",
            "work_experience",
            "education",
            "skills",
            "references",
        ]


class ProjectProposalSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    document_session = DocumentSessionSerializer(read_only=True)

    class Meta:
        model = ProjectProposal
        fields = [
            "id",
            "user",
            "document_session",
            "title",
            "description",
            "objectives",
            "methodology",
            "budget",
            "timeline",
            "conclusion",
        ]


class ProjectReportSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    document_session = DocumentSessionSerializer(read_only=True)

    class Meta:
        model = ProjectReport
        fields = [
            "id",
            "user",
            "document_session",
            "title",
            "literature_review",
            "methodology",
            "results",
            "discussion",
            "conclusion",
        ]
