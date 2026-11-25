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


class Motorista(models.Model):
    class CategoriaCNH(models.TextChoices):
        A = "A", "A"
        B = "B", "B"
        C = "C", "C"
        D = "D", "D"
        E = "E", "E"

    class TipoTransporte(models.TextChoices):
        PESSOAS = "PESSOAS", "Pessoas"
        MATERIAIS = "MATERIAIS", "Materiais"
        AMBOS = "AMBOS", "Ambos"

    class Status(models.TextChoices):
        ATIVO = "ATIVO", "Ativo"
        INATIVO = "INATIVO", "Inativo"

    nome = models.CharField("nome", max_length=100)
    cpf = models.CharField("CPF", max_length=14, unique=True)
    matricula = models.CharField("matrícula", max_length=20, unique=True)
    categoria_cnh = models.CharField(
        "categoria da CNH",
        max_length=1,
        choices=CategoriaCNH.choices,
    )
    tipo_transporte = models.CharField(
        "tipo de transporte",
        max_length=10,
        choices=TipoTransporte.choices,
    )
    status = models.CharField(
        "status",
        max_length=10,
        choices=Status.choices,
        default=Status.ATIVO,
    )

    class Meta:
        verbose_name = "motorista"
        verbose_name_plural = "motoristas"
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome} ({self.matricula})"