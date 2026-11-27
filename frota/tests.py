from django.test import TestCase
from django.urls import reverse

from .forms import VeiculoForm
from .models import Veiculo


class VeiculoTests(TestCase):
    def setUp(self):
        self.veiculo = Veiculo.objects.create(
            placa="ABC1D23",
            marca="Fiat",
            modelo="Uno",
            ano=2020,
            status=Veiculo.Status.ATIVO,
        )

    def test_t01_rejeitar_placa_duplicada(self):
        """T01: não deve permitir cadastrar dois veículos com a mesma placa."""
        dados = {
            "marca": "Toyota",
            "modelo": "Hilux",
            "ano": 2023,
            "placa": "abc1d23",
            "status": Veiculo.Status.ATIVO,
        }
        resposta = self.client.post(reverse("veiculo_criar"), data=dados)

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Já existe um veículo cadastrado com esta placa.")
        self.assertEqual(Veiculo.objects.count(), 1)

    def test_cadastrar_veiculo_valido(self):
        dados = {
            "marca": "Toyota",
            "modelo": "Hilux",
            "ano": 2023,
            "placa": "ghi4j56",
            "cor": "Prata",
            "combustivel": Veiculo.Combustivel.DIESEL,
            "categoria": Veiculo.Categoria.UTILITARIO,
            "tipo": "Caminhonete",
            "status": Veiculo.Status.ATIVO,
            "observacoes": "Uso em viagens.",
        }
        resposta = self.client.post(reverse("veiculo_criar"), data=dados)

        self.assertRedirects(resposta, reverse("veiculo_lista"))
        novo = Veiculo.objects.get(placa="GHI4J56")
        self.assertEqual(novo.cor, "Prata")

    def test_visualizar_e_editar_veiculo(self):
        resposta_detalhe = self.client.get(
            reverse("veiculo_detalhe", args=[self.veiculo.pk])
        )
        self.assertEqual(resposta_detalhe.status_code, 200)
        self.assertContains(resposta_detalhe, "ABC1D23")

        resposta_editar = self.client.post(
            reverse("veiculo_editar", args=[self.veiculo.pk]),
            data={
                "marca": "Fiat",
                "modelo": "Uno Way",
                "ano": 2021,
                "placa": "ABC1D23",
                "status": Veiculo.Status.ATIVO,
            },
        )
        self.assertRedirects(resposta_editar, reverse("veiculo_lista"))
        self.veiculo.refresh_from_db()
        self.assertEqual(self.veiculo.modelo, "Uno Way")

    def test_inativar_veiculo_sem_excluir_historico(self):
        resposta = self.client.post(reverse("veiculo_inativar", args=[self.veiculo.pk]))

        self.assertRedirects(resposta, reverse("veiculo_lista"))
        self.veiculo.refresh_from_db()
        self.assertEqual(self.veiculo.status, Veiculo.Status.INATIVO)
        self.assertEqual(Veiculo.objects.count(), 1)

    def test_nao_permite_escolher_em_manutencao_manualmente(self):
        form = VeiculoForm(
            data={
                "marca": "Volkswagen",
                "modelo": "Saveiro",
                "ano": 2022,
                "placa": "XYZ9K88",
                "status": Veiculo.Status.EM_MANUTENCAO,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("status", form.errors)