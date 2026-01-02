from django.db.models import TextChoices


class ChoicesCategoriaManutencao(TextChoices):
    TROCAR_OLEO = 'TO', 'Trocar Óleo'
    ALINHAMENTO = 'AL', 'Alinhamento'
    BALANCEAMENTO = 'BA', 'Balanceamento'
    REVISAO_GERAL = 'RG', 'Revisão Geral'
