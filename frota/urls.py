from django.urls import path

from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("veiculos/", views.veiculo_lista, name="veiculo_lista"),
    path("veiculos/novo/", views.veiculo_criar, name="veiculo_criar"),
    path("veiculos/<int:pk>/", views.veiculo_detalhe, name="veiculo_detalhe"),
    path("veiculos/<int:pk>/editar/", views.veiculo_editar, name="veiculo_editar"),
    path("veiculos/<int:pk>/inativar/", views.veiculo_inativar, name="veiculo_inativar"),
]