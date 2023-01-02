from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse,JsonResponse
#from rembg import remove
#from PIL import Image
from .aifile import *
from .functions import handleWhatsAppChat
from django.views.decorators.csrf import csrf_exempt
import json

def text_p(input_text):
     response = openai.Completion.create(
        model="text-davinci-003",
        prompt=input_text,
        max_tokens=2000,
        temperature=0.5,
        top_p=1,
        best_of=2,
        presence_penalty=0,
        frequency_penalty=0,
    )
     if 'choices' in response:
        if len(response['choices'])>0:
            generated_text = response['choices'][0]['text'].replace('\n', '<br>')
            
            return input_text + generated_text
        else:
            return ''
        
def generate_image_view(request):
    
    # Get the user's input from the request
    if request.method == 'POST':
        input_text = request.POST['message']
        response = image_processor_response(input_text)
        data = {'response': response}
        return JsonResponse(data)
    else:
       return render(request,"task/image-generator.html")

def text_processor_view(request):
    # Get the user's input from the request
    if request.method == 'POST':
   # if request.POST.get("input_text", "") != '\0':
        input_text = request.POST['message']
        # Generate Text
        response = text_p(input_text)
        data = {'response': response}
        #data = parse.process_text(response)
        return JsonResponse(data)
    else:
        return render(request,"task/text-processor.html")
    
    
def image_bg_remover_view(request):
   # Get the user's input from the request
    if request.method == 'POST':
        input_image = request.POST['original_image']
        # Load Image
        #response = Image.open(input_image)
         # remove background
       #output = remove(response)
        return render(request,"task/image-bg-remover.html")
        return JsonResponse({'response': output})
    else:
        return render(request,"task/image-bg-remover.html")
    

def business(request):
     return render(request,'business/index.html')

@csrf_exempt
def whatsAppWebHook(request):
    if request.method == 'POST':
        VERIFY_TOKEN = ''
        mode = request.GET['hub.mode']
        token = request.GET['hub.verify_token']
        challenge = request.GET['hub.challenge']
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return HttpResponse(challenge,status=200)
        else:
            return HttpResponse('error',status=403)
 
    if request.method =='POST':
        data = json.loads(request.body)
        if 'object' in data and 'entry' in data:
            if data['object'] == 'whatsapp_business_account':
                for entry in data['entry']:
                    phoneId = entry['changes'][0]['value']['metadata']['phone_number_id']
                    profileName = entry['changes'][0]['value']['contacts'][0]['profile']['name']
                    profileImage = entry['changes'][0]['value']['contacts'][0]['profile']['image']
                    whatsAppId =  entry['changes'][0]['value']['contacts'][0]['wa_id']
                    fromId =  entry['changes'][0]['value']['messages'][0]['from']
                    text =  entry['changes'][0]['value']['messages'][0]['text']['body']
                    
                    handleWhatsAppChat(fromId,profileName,phoneId,text)
                    
            else:
                pass
        else:
            pass
        
        return HttpResponse('success',status=200)
                    
