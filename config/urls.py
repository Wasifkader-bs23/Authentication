from django.contrib import admin
from django.urls import path
from django.urls import path, include
from accounts.views import *
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterAPI.as_view()),
    path('verify/',VerifyOTP.as_view()),
    path('login/',Login.as_view()),
    
]
