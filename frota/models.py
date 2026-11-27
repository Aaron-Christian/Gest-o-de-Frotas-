from django.db import models


class Veiculo(models.Model):
    class Status(models.TextChoices):
        ATIVO = "ATIVO", "Ativo"
        EM_MANUTENCAO = "EM_MANUTENCAO", "Em manutenção"
        INATIVO = "INATIVO", "Inativo"

    class Combustivel(models.TextChoices):
        FLEX = "FLEX", "Flex"
        GASOLINA = "GASOLINA", "Gasolina"
        ETANOL = "ETANOL", "Etanol"
        DIESEL = "DIESEL", "Diesel"
        ELETRICO = "ELETRICO", "Elétrico"
        HIBRIDO = "HIBRIDO", "Híbrido"

    class Categoria(models.TextChoices):
        LEVE = "LEVE", "Leve"
        UTILITARIO = "UTILITARIO", "Utilitário"
        PESADO = "PESADO", "Pesado"
        MOTO = "MOTO", "Moto"

    placa = models.CharField("placa", max_length=10, unique=True)
    marca = models.CharField("marca", max_length=50)
    modelo = models.CharField("modelo", max_length=50)
    ano = models.PositiveSmallIntegerField("ano do modelo")
    cor = models.CharField("cor", max_length=30, blank=True, default="")
    renavam = models.CharField("RENAVAM", max_length=20, blank=True, default="")
    chassi = models.CharField("chassi", max_length=30, blank=True, default="")
    combustivel = models.CharField(
        "combustível",
        max_length=15,
        choices=Combustivel.choices,
        blank=True,
        default="",
    )
    categoria = models.CharField(
        "categoria",
        max_length=15,
        choices=Categoria.choices,
        blank=True,
        default="",
    )
    tipo = models.CharField("tipo", max_length=30, blank=True, default="")
    status = models.CharField(
        "status",
        max_length=20,
        choices=Status.choices,
        default=Status.ATIVO,
    )
    observacoes = models.TextField("observações", blank=True, default="")

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