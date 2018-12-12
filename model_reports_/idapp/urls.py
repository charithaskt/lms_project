from django.urls import path
from . import views

urlpatterns = [
    path('', views.id_card, name='id-card'),
    #path('index',views.index ,name='index')

]


