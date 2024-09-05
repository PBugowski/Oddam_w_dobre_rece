"""
URL configuration for Oddam_w_dobre_ręce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from Oddam_w_dobre_ręce_app import views as app_views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', app_views.LandingPageView.as_view(), name='landing-page'),
    path('add_donation/', app_views.AddDonationView.as_view(), name='add-donation'),
    path('login/', app_views.LoginView.as_view(), name='login'),
    path('register/', app_views.RegisterView.as_view(), name='register'),
    path('logout/', app_views.LogoutView.as_view(), name='logout'),
    path('profile/', app_views.ProfileView.as_view(), name='profile'),
    path('my_donations/', app_views.MyDonationsView.as_view(), name='my-donations'),
]
