from django.urls import path

from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("veiculos/", views.veiculo_lista, name="veiculo_lista"),
]