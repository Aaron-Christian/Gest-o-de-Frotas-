from django.db.models import Q
from django.shortcuts import redirect, render

from .models import Veiculo


def inicio(request):
    return redirect("veiculo_lista")


def veiculo_lista(request):
    veiculos = Veiculo.objects.all()
    busca = request.GET.get("busca", "").strip()
    status_atual = request.GET.get("status", "").strip()

    if busca:
        veiculos = veiculos.filter(
            Q(placa__icontains=busca)
            | Q(marca__icontains=busca)
            | Q(modelo__icontains=busca)
        )

    if status_atual in Veiculo.Status.values:
        veiculos = veiculos.filter(status=status_atual)

    contexto = {
        "veiculos": veiculos,
        "busca": busca,
        "status_atual": status_atual,
        "status_opcoes": Veiculo.Status.choices,
    }
    return render(request, "frota/veiculo_lista.html", contexto)
