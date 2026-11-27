from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import VeiculoForm
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


def veiculo_criar(request):
    if request.method == "POST":
        form = VeiculoForm(request.POST)
        if form.is_valid():
            veiculo = form.save()
            messages.success(request, f"Veículo {veiculo.placa} cadastrado com sucesso.")
            return redirect("veiculo_lista")
        messages.error(request, "Corrija os erros no formulário antes de salvar.")
    else:
        form = VeiculoForm()

    contexto = {
        "form": form,
        "titulo": "Novo veículo",
        "botao": "Cadastrar veículo",
    }
    return render(request, "frota/veiculo_form.html", contexto)


def veiculo_detalhe(request, pk):
    veiculo = get_object_or_404(Veiculo, pk=pk)
    return render(request, "frota/veiculo_detalhe.html", {"veiculo": veiculo})


def veiculo_editar(request, pk):
    veiculo = get_object_or_404(Veiculo, pk=pk)

    if request.method == "POST":
        form = VeiculoForm(request.POST, instance=veiculo)
        if form.is_valid():
            veiculo = form.save()
            messages.success(request, f"Veículo {veiculo.placa} atualizado com sucesso.")
            return redirect("veiculo_lista")
        messages.error(request, "Corrija os erros no formulário antes de salvar.")
    else:
        form = VeiculoForm(instance=veiculo)

    contexto = {
        "form": form,
        "veiculo": veiculo,
        "titulo": f"Editar veículo {veiculo.placa}",
        "botao": "Salvar alterações",
    }
    return render(request, "frota/veiculo_form.html", contexto)


@require_POST
def veiculo_inativar(request, pk):
    veiculo = get_object_or_404(Veiculo, pk=pk)

    if veiculo.status == Veiculo.Status.INATIVO:
        messages.info(request, f"O veículo {veiculo.placa} já está inativo.")
    else:
        veiculo.status = Veiculo.Status.INATIVO
        veiculo.save(update_fields=["status"])
        messages.success(request, f"Veículo {veiculo.placa} inativado com sucesso.")

    return redirect("veiculo_lista")