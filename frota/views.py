from django.shortcuts import render


def inicio(request):
    contexto = {"mensagem": "Olá, frota!"}
    return render(request, "frota/inicio.html", contexto)
