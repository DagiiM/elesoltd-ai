
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/',views.dashboard,name='dashboard'),
    #path('register/', views.register, name='register'),
    #path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
    #path('password_change/', views.password_change, name='password_change'),
    #path('password_change/done/', views.password_change_done, name='password_change_done'),
    #path('password_reset/', views.password_reset, name='password_reset'),
    #path('password_reset/done/', views.password_reset_done, name='password_reset_done'),
    #path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', views.password_reset_complete, name='password_reset_complete'),
]


'''
from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'api/users/', views.UserViewSet)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', include(router.urls)),
    #path('users/login/', views.UserViewSet.as_view({'post': 'login'}), name='login'),
    path('auth/', obtain_auth_token, name='api_token_auth'),
    path('login/',views.user_login,name='login'),
   
    #path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('api-auth/', include('rest_framework.urls')),
]

'''

from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users/', UserViewSet, basename='user')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    
    path('dashboard/',views.dashboard,name='dashboard'),
    path('api/users/login/', views.UserViewSet.as_view({'post': 'login'}), name='login'),
    path('reset/', views.UserViewSet.as_view({'post': 'password_reset'}), name='password_reset'),
    path('users/change-password/', views.UserViewSet.as_view({'post': 'change_password'}), name='change_password'),
    #path('users/logout/', views.UserViewSet.as_view({'post': 'logout'}), name='logout'),
    path('users/activate/<uidb64>/<token>/',views.activate,name='activate'),
    #path('reset/<uidb64>/<token>/', views.UserViewSet.as_view({'post','password_reset_confirm'}), name='password_reset_confirm'),
    path('register/', views.register, name='register'),
    path('login/', views.view_login, name='view_login'),
    path('logout/', views.view_logout, name='view_logout'),
    path('forgot_password/', views.view_forgot_password, name='view_forgot_password'),
    #path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset-password',views.resetPassword,name='resetPassword'), 
    #path('reset/', views.password_reset, name='password_reset'),
    path('resetpassword_validate/<uidb64>/<token>/',views.resetpassword_validate,name='resetpassword_validate'), 
    path('reset-password',views.resetPassword,name='resetPassword'), 
]


api_urlpatterns = [
    
]
