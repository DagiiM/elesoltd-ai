from django.shortcuts import render
from django.conf import settings
#import pdfkit
from django.template.loader import get_template
import os

# Create your views here.

def document_landing_page(request):
    return render(request,'business/index.html')

def document_create_business_plan_page(request):
    return render(request,'business/business_plan.html')
def document_create_resume_page(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        address = request.POST['address']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        professional_summary = request.POST['professional_summary']
        job_title = request.POST['job_title']
        duties = request.POST['duties']
        school_name = request.POST['school_name']
        degree = request.POST['degree']
        dates_of_attendance = request.POST['dates_of_attendance']
        skills = request.POST['skills']
        reference_name = request.POST['reference_name']
        reference_contact_info = request.POST['reference_contact_info']
        reference_relationship = request.POST['reference_relationship']
        
        resume_prompt = "Generate a Resume Based on the following : My Contact Information: {fullname} , address: {address}, email: {email}, professional summary: {professional_summary}. My previous job title is {job_title} where my duty was {duties}. The school I attended: {school_name}. Degree : {degree},my skills:{skills}, my rereferences : {reference_name} {reference_contact_info} {reference_relationship}" 
        cover_letter_prompt = "Please Generate a cover for me. my name {fullname} skills:{skills}, applying to {apply_to}, {letter_details}"
    
    return render(request,'business/resume.html')
def document_create_project_proposal_page(request):
    return render(request,'business/project_proposal.html')
def document_create_project_report_page(request):
    return render(request,'business/project_report.html')


def createCoverLetterPDF(coverLetter):
    # Variables we need
    
    #The name of your PDF file
    filename ='cover_letter.pdf'

    #HTML FIle to be converted to PDF - inside your Django directory
    template = get_template('business/cover_letter_doc.html')

    #Add any context variables you need to be dynamically rendered in the HTML
    context = {}

    #Render the HTML
    html = template.render(context)

    #Options - Very Important [Don't forget this]
    options = {
        'encoding': 'UTF-8',
        'javascript-delay':'1000', #Optional
        'enable-local-file-access': None, #To be able to access CSS
        'page-size': 'A4',
        'custom-header' : [
            ('Accept-Encoding', 'gzip')
        ],
    }
    #Javascript delay is optional

    #Remember that location to wkhtmltopdf
    config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

     #Saving the File
    file_path = settings.MEDIA_ROOT + '/cover_letters/{}/'.format(profile.uniqueId)
    os.makedirs(file_path, exist_ok=True)
    pdf_save_path = file_path+filename
    #Save the PDF
    pdfkit.from_string(html, pdf_save_path, configuration=config, options=options)
    
    doc_url = 'cover_letters/{}/{}'.format(profile.uniqueID,filename)
    
    https_path = 'https://eleso.online'+doc_url

    #Return
    return https_path


def createResumePDF(resume):
    
    #The name of your PDF file
    filename = 'resume.pdf'

    #HTML FIle to be converted to PDF - inside your Django directory
    template = get_template('resumes/resume_doc.html')

    #Add any context variables you need to be dynamically rendered in the HTML
    context = {'data':resume}

    #Render the HTML
    html = template.render(context)

    #Options - Very Important [Don't forget this]
    options = {
        'encoding': 'UTF-8',
        'javascript-delay':'1000', #Optional
        'enable-local-file-access': None, #To be able to access CSS
        'page-size': 'A4',
        'custom-header' : [
            ('Accept-Encoding', 'gzip')
        ],
    }
    #Javascript delay is optional

    #Remember that location to wkhtmltopdf
    config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

     #Saving the File
    file_path = settings.MEDIA_ROOT + '/resumes/'
    os.makedirs(file_path, exist_ok=True)
    pdf_save_path = file_path+filename
    #Save the PDF
    pdfkit.from_string(html, pdf_save_path, configuration=config, options=options)
    
   # doc_url = 'resumes/{}/{}'.format(profile.uniqueID,filename)
    
   # https_path = 'https://eleso.online'+doc_url

    #Return
    return httpResponse('Successfully created')