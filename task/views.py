from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse,JsonResponse
#from rembg import remove
#from PIL import Image
from .aifile import *
from .functions import handleWhatsAppChat
from django.views.decorators.csrf import csrf_exempt
import json
from . models import *
from django.shortcuts import render
from .models import Order

'''
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
        
        
   '''
    
        
        
def text_p(input_text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Write a creative ad for the following product to run on Facebook aimed at parents:\n\nProduct: Learning Room is a virtual environment to help students from kindergarten to high school excel in school.",
        temperature=0.5,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )
    
    if 'choices' in response:
        if len(response['choices'])>0: 
            completions = response['choices'][0]['text'].replace('\n', '<br>')
            return input_text+completions    
        else:
            return 'There was an error Processing your request. Please try again'
    
        
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
                    


from django.shortcuts import render, HttpResponseRedirect
from .forms import CheckoutForm
from .models import Order, OrderItem, Address

def checkout(request):
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create a new Order object
            order = Order()
            order.name = form.cleaned_data["name"]
            order.email = form.cleaned_data["email"]
            order.phone = form.cleaned_data["phone"]
            # Create a new Address object for shipping address
            shipping_address = Address()
            shipping_address.street = form.cleaned_data["shipping_street"]
            shipping_address.city = form.cleaned_data["shipping_city"]
            shipping_address.state = form.cleaned_data["shipping_state"]
            shipping_address.zip_code = form.cleaned_data["shipping_zip_code"]
            shipping_address.save()
            order.shipping_address = shipping_address
            # Create a new Address object for billing address
            billing_address = Address()
            billing_address.street = form.cleaned_data["billing_street"]
            billing_address.city = form.cleaned_data["billing_city"]
            billing_address.state = form.cleaned_data["billing_state"]
            billing_address.zip_code = form.cleaned_data["billing_zip_code"]
            billing_address.save()
            order.billing_address = billing_address
            order.payment_method = form.cleaned_data["payment_method"]
            order.total_price = calculate_total_price()  # TODO: Write function to calculate total price
            order.status = "pending"
            order.save()
            # Create a new OrderItem object for each item in the cart
            for item in get_cart_items():  # TODO: Write function to get items in the cart
                order_item = OrderItem()
                order_item.name = item.name
                order_item.price = item.price
                order_item.quantity = item.quantity
                order_item.order = order
                order_item.save()
            # Redirect to confirmation page
            return HttpResponseRedirect("/checkout/confirmation")
    else:
        form = CheckoutForm()
    return render(request, "checkout.html", {"form": form})
