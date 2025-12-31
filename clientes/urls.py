from django.urls import path
from . import views

urlpatterns = [
    path('', views.clientes, name='clientes'),
    path('/atualizar_cliente/', views.att_cliente, name='atualizar_cliente'),
]
