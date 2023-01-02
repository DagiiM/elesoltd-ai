from django.db import models
from django.conf import settings
import pdfkit
from django.template.loader import get_template
import os
import requests
import asyncio
from .aifile import *
loop = asyncio.new_event_loop()


def sendWhatsappMessage(phoneNumber, message):
    headers = {"Authorization":settings.WHATSAPP_TOKEN}
    payload = {
        "messaging_product":"whatsapp",
        "recipient_type":"individual",
        "to":phoneNumber,
        "type":"text",
        "text":{"body":message}
    }
    response = requests.post(settings.WHATSAPP_URL,headers=headers,json=payload)
    ans = response.json

def createPDF(chat,businessPlan):
    # Variables we need
    profile = chat.profile
    
    #The name of your PDF file
    filename = businessPlan.uniqueId+'.pdf'

    #HTML FIle to be converted to PDF - inside your Django directory
    template = get_template('business/document.html')

    #Add any context variables you need to be dynamically rendered in the HTML
    context = {}
    context['date']=businessPlan.date_created
    context['business_name']=chat.business_name
    context['company_description'] = businessPlan.company_description
    context['market_analysis'] = businessPlan.market_analysis
    context['swot_analysis'] = businessPlan.swot_analysis
    context['product_detail'] = businessPlan.product_detail
    context['marketing_strategy'] = businessPlan.marketing_strategy

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
    file_path = settings.MEDIA_ROOT + '/business_plans/{}/'.format(profile.uniqueId)
    os.makedirs(file_path, exist_ok=True)
    pdf_save_path = file_path+filename
    #Save the PDF
    pdfkit.from_string(html, pdf_save_path, configuration=config, options=options)
    
    doc_url = 'business_plans/{}/{}'.format(profile.uniqueID,filename)
    
    https_path = 'https://eleso.online'+doc_url

    #Return
    return https_path

def buildBusinessPlan(chat): 
    company_description = companyDescriptionProgress(chat.business_name,chat.business_type,chat.country,chat.product_service,chat.short_description,chat.years,chat.progress)
    market_analysis= marketAnalysis(chat.business_name,chat.product_service,chat.short_description)
    swot_analysis=swotAnalysis(chat.business_name,chat.product_service,chat.short_description)
    product_detail=productDetail(chat.business_name,chat.product_service,chat.short_description)
    marketing_strategy=marketingStrategy(chat.business_name,chat.product_service,chat.short_description)
    
    businessPlan = BusinessPlan.objects.create(
        profile=chat.profile,
        company_description=company_description,
        market_analysis=market_analysis,
        swot_analysis=swot_analysis,
        product_detail=product_detail,
        marketing_strategy=marketing_strategy
    )
    BusinessPlan.save()
    
    return businessPlan

def createNewBusinessPlan(chat):
    # 1. Build the business plan
    businessPlan = buildBusinessPlan(chat)
    
    # 2. Create the Document PDF
    doc_url = createPDF(chat,businessPlan)
    
    # 3. Send the Document Link to the User
    message = '😀 Your Business Plan is Ready 👇 👇 \n\n {}'.format(doc_url)
    sendWhatsappMessage(chat.profile.phoneNumber, message)
    # 4. Delete the chat at the end
    chat.delete()
    
def handleWhatsAppChat(fromId,profileName,phoneId,Text):
    # Check if there is a chat session
    try:
        chat = ChatSession.objects.get(phone__profileNumber=fromId)
    except ChatSession.DoesNotExist:
        #check that this user does already exist
        if User.objects.filter(username=phoneId).exists():
            user = User.objects.get(username=phoneId)
            user_profile = user.profile
        else:
            # Create a new user
            user = User.objects.create(
                profile=profileName,
                phone=phoneId,
                username=phoneId,
                email='test@test.com',
                first_name=profileName.first_name,
                last_name=profileName.last_name
                )
            # Creating profile for the user
            user_profile = Profile.objects.create(
                user=user,
                phoneNumber=fromId,
                phoneId=phoneId
            )
            
            user_profile.save()
        # Create a new chat session
        chat = ChatSession.objects.create(profile=user_profile)
        message = "Welcome to AI Bunesiness Plan Creator 😀 \n I am going to take you through a process of creating a well polished Business Plan, Right hereon Whatsapp. To get Started Enter your Business Name and Email Address:"
        sendWhatsappMessage(fromId, message)
        return ''
    
    # When you return 
    # Continue with the function
    if chat.business_name:
        if chat.business_type:
            if chat.country:
                if chat.product_service:
                    if chat.short_description:
                        if chat.years:
                            if chat.progress:
                                # Do something else
                                message = "Our AI is working on it Give us a moment, we will message you when your Business Plan is ready"
                                sendWhatsappMessage(fromId,message)
                                createNewBusinessPlan(chat)      
                                #Run in the background              
                                loop.run_in_executor(None,createNewBusinessPlan,chat)         
                                return ''
                            else:
                                chat.progress = text
                                chat.save()
                                message="Great we have everything we need to build your business plan. \n _'Enter anything to Continue ...'_"
                                sendWhatsappMessage(fromId,message)
                                return ''
                        else:
                            try:
                                years = int(text.replace(' ',''))
                                chat.years = years
                                chat.save()
                                  # Send next message
                                message = 'How much traction have you made in your business?\n e.g _"We have clients already paying for our services."_'
                                sendWhatsappMessage(fromId,message)
                                return ''
                        
                            except:
                                message = 'Please enter a number like 1, 2 etc.'
                                sendWhatsappMessage(fromId,message)
                                return ''
                    else:
                        chat.short_description = text
                        chat.save()
                        # Send next message
                        message = "How many years have you been operating your business? Enter a number like 1 or 2."
                        sendWhatsappMessage(fromId,message)
                        return ''
                else:
                    chat.product_service = text
                    chat.save()
                    
                    # Send next message
                    message = "Describe your business idea in one or two sentences. Be as precise as you can."
                    sendWhatsappMessage(fromId,message)
                    return ''
            else:
                chat.country = text
                chat.save()
                # Send next message
                message ="What Product or Service will your business be providing?"
                sendWhatsappMessage(fromId,message)
                return ''
        else:
            # Test for the number
            try:
                type = int(text.replace(' ', ''))
                if type == 1:
                    chat.business_type = '(Pty) Ltd'
                    chat.save()
                    # Send next message
                    message = "Which Country are you from ?"
                    sendWhatsappMessage(fromId,message)
                    return ''
                if type == 2:
                    chat.business_type = 'Non-Profit'
                    chat.save()
                    # Send next message
                    message = "Which Country are you from ?"
                    sendWhatsappMessage(fromId,message)
                    return ''
                if type == 3:
                    chat.business_type = 'Partnership'
                    chat.save()
                    # Send next message
                    message = "Which Country are you from ?"
                    sendWhatsappMessage(fromId,message)
                    return ''
            except:
                # Send next message
                message ="Please select the type of business. Enter the number Corresponding to the type of business:\n 1.(Pty) Ltd  \2. Non-Profit  \3. Partnership \n\n Enter just the number."
                sendWhatsappMessage(fromId,message)
                return ''
                    
                


















