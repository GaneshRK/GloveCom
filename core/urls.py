from django.urls import path
from . import views
from django.shortcuts import render
app_name = 'core'
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('contact/success/', views.contact_success, name='contact_success'),
    path('privacy-policy/', lambda r: render(r,'core/privacy.html'), name='privacy'),
    path('terms/', lambda r: render(r,'core/terms.html'), name='terms'),
]
