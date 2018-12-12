from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('', views.pay, name='pay'),
    path('check', views.check, name='check'),
    path('status/', views.status, name='status'),
    path('fineform/', views.pay_fine, name='payfine'),
]
