import os
import openai
from django.conf import settings

# Set the API key
openai.api_key = settings.OPENAI_API_KEY

def text_processor_response(input_text):
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
            generated_text = response['choices'][0]['text'].replace('\n', '<br>').replace('\t', '&emsp')
           # output_string = replace_special_characters(generated_text)
            return input_text + generated_text
        else:
            return ''


def image_processor_response(input_text): 
   response = openai.Image.create(
    prompt=input_text,
    n=2,
    size="512x512"
    )
   return response

def companyDescriptionProgress(business_name,business_type,country,product_service,short_description,years,progress):
    question = ""
    response = text_processor_response(question)
    return response

def companyDescription(business_name,business_type,country,product_service,short_description,years):
    question = ""
    response = text_processor_response(question)
    return response
    
def marketAnalysis(business_name,product_service,short_description):
    question = "Generate a market analysis for a business plan for the following business using the guildelines provided"
    response = text_processor_response(question)
    return response

def swotAnalysis(business_name,product_service,short_description):
    question = "Generate a swot analysis for a business plan for the following business using the guildelines provided"
    response = text_processor_response(question)
    return response

def productDetail(business_name,product_service,short_description):
    question = "Generate a market analysis for a business plan for the following business using the guildelines provided"
    response = text_processor_response(question)
    return response 

def marketingStrategy(business_name,product_service,short_description):
    question = "Generate a market analysis for a business plan for the following business using the guildelines provided"
    response = text_processor_response(question)
    return response     