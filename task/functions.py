from .models import *
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
    
def handleWhatsAppChat(fromId,profileName,phoneId,text):
    # Check if there is a ch at session
    try:
        chat = ChatSession.objects.get(profile__profileNumber=fromId)
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
                email=phoneId+'@test.eleso.ltd',
                password='@'+phoneId,
                first_name=profileName,
                #email= email_address
                #first_name=profileName.first_name,
                #last_name=profileName.last_name
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
        message = "Welcome to AI Bunesiness Plan Creator 😀 \n I am going to take you through the process of creating a well polished Business Plan, Right hereon Whatsapp. To get Started Enter your Business Name and Email Address:"
        sendWhatsappMessage(fromId, message)
        #return ''
   
   
   
# When returns
    if not chat.business_name:
        try:
            type = int(text.replace(' ', ''))
            if type == 1:
                chat.business_type = '(Pty) Ltd'
                sendWhatsappMessage(fromId, 'Which country are you from?')
            elif type == 2:
                chat.business_type = 'Non-Profit'
                sendWhatsappMessage(fromId, 'Which country are you from?')
            elif type == 3:
                chat.business_type = 'Partnership'
                sendWhatsappMessage(fromId, 'Which country are you from?')
            else:
                sendWhatsappMessage(fromId, "Please try again. Enter the number corresponding to your business Type: Enter \n 1. (Pty) Ltd \n 2. Non-Profit \n 3. Partnership")
        except ValueError:
            sendWhatsappMessage(fromId, "Please try again. Enter the number corresponding to your business Type: Enter \n 1. (Pty) Ltd \n 2. Non-Profit \n 3. Partnership")
    elif not chat.country:
        chat.country = text
        sendWhatsappMessage(fromId, 'What product or service wil be your business providing?')
    elif not chat.product_service:
        chat.product_service = text
        sendWhatsappMessage(fromId, 'Describe your business idea in 1 or 2 services.')
    elif not chat.short_description:
        chat.short_description = text
        sendWhatsappMessage(fromId, 'How many years have you been in business for? Enter a number like 1 0r 2.')
    elif not chat.years:
        try:
            years = int(text.replace(' ', ''))
            chat.years = years
            sendWhatsappMessage(fromId, "How much traction have you made in your business?")
        except ValueError:
            sendWhatsappMessage(fromId, "Please try again, enter a number like 1 or 2")
    elif not chat.progress:
        chat.progress = text
        sendWhatsappMessage(fromId, "Great! We have everything to create your business plan")
        loop.run_in_executor(None, createNewBusinessPlan, chat)
    else:
        sendWhatsappMessage(fromId, "We are working on your business plan. Should be ready shortly.")
        createNewBusinessPlan(chat)




'''

## When you return
    if chat.business_name:
        if chat.business_type:
           if chat.country:
               if chat.product_service:
                   if chat.short_description:
                       if chat.years:
                           if chat.progress:
                               message = "We are working on your business plan. Should be ready shortly."
                               sendWhatsappMessage(fromId, message)
                               createNewBusinessPlan(chat)
                                #Run in the background              
                               loop.run_in_executor(None,createNewBusinessPlan,chat)         
                               return ''
                           else:
                                chat.progress = text
                                chat.save()
                                # Send Next Question
                                message = "Great! We have everything to create your business Plan"
                                sendWhatsappMessage(fromId, message)
                                return ''
                       else:
                            try:
                                years = int(text.replace(' ', ''))
                                chat.years = years
                                chat.save()
                                # Send Next Question
                                message = "How much traction have you made in your business?"
                                sendWhatsappMessage(fromId, message)
                                return ''
                            except:
                                message = "Please try again, enter a number like 1 or 2"
                                sendWhatsappMessage(fromId, message)
                                return ''
                   else:
                        chat.short_description = text
                        chat.save()
                        # Send Next Question
                        message = 'How many years have you been in business for? Enter a number like 1 0r 2.'
                        sendWhatsappMessage(fromId, message)
                        return ''
               else:
                    chat.product_service = text
                    chat.save()
                    message = 'Describe your business idea in 1 or 2 services.'
                    sendWhatsappMessage(fromId, message)
                    return ''
           else:
                chat.country = text
                chat.save()
                # Send Next Question
                message = 'What product or service wil be your business providing?'
                sendWhatsappMessage(fromId, message)
                return ''    
    else:
            try:
                type = int(text.replace(' ', ''))
                if type == 1:
                    chat.business_type = '(Pty) Ltd'
                    chat.save()
                    # Send Next Question  
                    message = 'Which country are you from?'
                    sendWhatsappMessage(fromId, message)
                    return ''
                elif type == 2:
                    chat.business_type = 'Non-Profit'
                    chat.save()
                    # Send Next Question  
                    message = 'Which country are you from?'
                    sendWhatsappMessage(fromId, message)
                    return ''
                elif type == 3:
                    chat.business_type = 'Partnership'
                    chat.save()
                    # Send Next Question
                    message = 'Which country are you from?'
                    sendWhatsappMessage(fromId, message)
                    return ''
                else:
                    message = "Please try again. Enter the number corresponding to your business Type: Enter \n 1. (Pty) Ltd \n 2. Non-Profit \n 3. Partnership"
                    sendWhatsappMessage(fromId, message)
                    return ''
            except:
                message = "Please try again. Enter the number corresponding to your business Type: Enter \n 1. (Pty) Ltd \n 2. Non-Profit \n 3. Partnership"
                sendWhatsappMessage(fromId, message)   
                return ''  
    else:
        chat.business_name = text
        chat.save()
        # Send Next Question
        message = "Please select the type of business. Enter the number corresponding to your business Type: Enter \n 1. (Pty) Ltd \n 2. Non-Profit \n 3. Partnership"
        sendWhatsappMessage(fromId, message)
        return ''   
        
'''
















