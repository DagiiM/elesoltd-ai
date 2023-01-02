from django.urls import path
from . import views

urlpatterns = [
    path('', views.text_processor_view, name="creator"),
    path('image-generation-with-ai', views.generate_image_view, name="generate-image"),
    path('image-bg-remover', views.image_bg_remover_view, name="bg-remover"),
   #path('pdf-test', views.createPDF, name="pdf-test"),
]
