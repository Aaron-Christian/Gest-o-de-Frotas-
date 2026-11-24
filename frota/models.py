from django.db import models


class Veiculo(models.Model):
    class Status(models.TextChoices):
        ATIVO = "ATIVO", "Ativo"
        EM_MANUTENCAO = "EM_MANUTENCAO", "Em manutenção"
        INATIVO = "INATIVO", "Inativo"

    placa = models.CharField("placa", max_length=10, unique=True)
    marca = models.CharField("marca", max_length=50)
    modelo = models.CharField("modelo", max_length=50)
    ano = models.PositiveSmallIntegerField("ano do modelo")
    status = models.CharField(
        "status",
        max_length=20,
        choices=Status.choices,
        default=Status.ATIVO,
    )

    class Meta:
        verbose_name = "veículo"
        verbose_name_plural = "veículos"
        ordering = ["placa"]

    def __str__(self):
        return f"{self.placa} - {self.marca} {self.modelo}"