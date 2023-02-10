from django.urls import path
from authentication import views

urlpatterns = [
    path('dashboard/',views.dashboard,name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
    path('password_change/', views.password_change, name='password_change'),
    path('password_change/done/', views.password_change_done, name='password_change_done'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('password_reset/done/', views.password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', views.password_reset_complete, name='password_reset_complete'),
]
