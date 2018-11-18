from django.urls import path
from . import views

urlpatterns = [
    path('barcode/', views.index, name='barcode'),
 
]


