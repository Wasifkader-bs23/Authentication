from django.contrib import admin
from django.urls import path
from django.urls import path, include

from accounts.views import *
from accounts import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterAPI.as_view()),
    path('verify/',VerifyOTP.as_view()),
    path('login/',Login.as_view()),
    path('user-view/',UserView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]
