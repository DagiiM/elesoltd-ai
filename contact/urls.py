from django.urls import path
from . import views

urlpatterns = [
    path('hire-request', views.hire_request, name="hire_request"),
     path('support', views.support_request, name="support_request"),
    path('about-us', views.about, name="about"),
    path('privacy-policy', views.privacy_policy, name="privacy_policy"),
    path('terms-and-conditions', views.terms_and_conditions, name="terms_conditions"),
]
