from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"
    
class Carro(models.Model):
    cliente = models.ForeignKey(Cliente, related_name='carros', on_delete=models.CASCADE)
    lavagens = models.IntegerField(default=0)
    consertos = models.IntegerField(default=0)
    carro = models.CharField(max_length=100)
    placa = models.CharField(max_length=10, unique=True)
    ano = models.IntegerField()

    def __str__(self):
        return f"{self.carro} - {self.placa}"