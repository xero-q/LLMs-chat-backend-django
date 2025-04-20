"""
URL configuration for ollamabackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from chat.views import CustomTokenObtainPairView, SignupView


urlpatterns = [
    path("admin", admin.site.urls),
    path("api/", include("chat.urls")),
    path(
        "api/auth/login", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path("api/auth/signup", SignupView.as_view(), name="signup_view"),
    path("api/auth/refresh", TokenRefreshView.as_view(), name="token_refresh"),
]
