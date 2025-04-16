from django.db import models

# Create your models here.

class Relatorio(models.Model):
    id = models.AutoField(primary_key=True)

    nome_usuario = models.CharField(max_length=100)
    numero_mesa = models.IntegerField()
    data_hora = models.DateTimeField(auto_now_add=True)
    tipo_desconto = models.CharField(max_length=50, default='Nenhum')
    tipo_pagamento = models.CharField(max_length=50)
    desconto = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade_pedidos = models.IntegerField()
    


    def __str__(self):
        return f"Relatório Mesa {self.numero_mesa} - {self.data_hora.strftime('%d/%m/%Y %H:%M')}"