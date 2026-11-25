from django.contrib import admin

from .models import Motorista, Veiculo

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ("placa", "marca", "modelo", "ano", "status")
    list_filter = ("status", "marca")
    search_fields = ("placa", "marca", "modelo")
@admin.register(Motorista)
class MotoristaAdmin(admin.ModelAdmin):
    list_display = ("nome", "cpf", "matricula", "categoria_cnh", "tipo_transporte", "status")
    list_filter = ("status", "categoria_cnh", "tipo_transporte")
    search_fields = ("nome", "cpf", "matricula")