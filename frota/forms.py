from django import forms

from .models import Veiculo


class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = [
            "marca",
            "modelo",
            "ano",
            "placa",
            "cor",
            "renavam",
            "chassi",
            "combustivel",
            "categoria",
            "tipo",
            "status",
            "observacoes",
        ]
        widgets = {
            "marca": forms.TextInput(attrs={"placeholder": "Ex.: Fiat"}),
            "modelo": forms.TextInput(attrs={"placeholder": "Ex.: Strada"}),
            "ano": forms.NumberInput(attrs={"placeholder": "Ex.: 2024"}),
            "placa": forms.TextInput(attrs={"placeholder": "Ex.: ABC1D23"}),
            "cor": forms.TextInput(attrs={"placeholder": "Ex.: Prata"}),
            "renavam": forms.TextInput(attrs={"placeholder": "Ex.: 12345678901"}),
            "chassi": forms.TextInput(attrs={"placeholder": "Ex.: 9BWZZZ377VT004251"}),
            "tipo": forms.TextInput(attrs={"placeholder": "Ex.: Passeio, Van, Caminhonete"}),
            "observacoes": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Observações opcionais sobre o veículo",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk and self.instance.status == Veiculo.Status.EM_MANUTENCAO:
            self.fields["status"].disabled = True
            self.fields["status"].help_text = (
                "Veículo em manutenção: o status muda automaticamente ao concluir a manutenção."
            )
        else:
            self.fields["status"].choices = [
                (Veiculo.Status.ATIVO, Veiculo.Status.ATIVO.label),
                (Veiculo.Status.INATIVO, Veiculo.Status.INATIVO.label),
            ]

    def clean_placa(self):
        placa = self.cleaned_data["placa"].strip().upper()
        consulta = Veiculo.objects.filter(placa__iexact=placa)
        if self.instance.pk:
            consulta = consulta.exclude(pk=self.instance.pk)
        if consulta.exists():
            raise forms.ValidationError("Já existe um veículo cadastrado com esta placa.")
        return placa

    def clean_chassi(self):
        return self.cleaned_data.get("chassi", "").strip().upper()

    def clean_ano(self):
        ano = self.cleaned_data["ano"]
        if ano < 1900 or ano > 2100:
            raise forms.ValidationError("Informe um ano válido entre 1900 e 2100.")
        return ano

    def clean_status(self):
        if self.instance.pk and self.instance.status == Veiculo.Status.EM_MANUTENCAO:
            return Veiculo.Status.EM_MANUTENCAO
        status = self.cleaned_data["status"]
        if status == Veiculo.Status.EM_MANUTENCAO:
            raise forms.ValidationError(
                "O status 'Em manutenção' só pode ser definido ao abrir uma manutenção."
            )
        return status