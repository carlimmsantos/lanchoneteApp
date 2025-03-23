from django.db import models
from apps.produtos.models import Produto

class Mesa(models.Model):
    numero = models.IntegerField()
    status = models.BooleanField(default=False)


    def __str__(self):
        return f'Mesa {self.numero}'

"""class Pedido(models.Model):
    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('fechado', 'Fechado'),
    ]

    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE, related_name='pedidos')
    valor = models.FloatField(default=0.0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='aberto')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Pedido {self.id} - Mesa {self.mesa.numero}'
    
class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='itens')
    quantidade = models.IntegerField(default=1)
    subtotal = models.FloatField()

    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome} (Pedido {self.pedido.id})'

    def save(self, *args, **kwargs):
        # Calcula o subtotal automaticamente ao salvar
        self.subtotal = self.quantidade * self.produto.custo
        super().save(*args, **kwargs)"""