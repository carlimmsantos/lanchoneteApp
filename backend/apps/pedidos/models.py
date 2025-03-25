from django.db import models
from apps.mesas.models import Mesa

# Create your models here.

class Pedido (models.Model):
    id = models.AutoField(primary_key=True)
    quantidade = models.IntegerField()

    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE, 
                             related_name="pedidos",
                             null=False,
                             blank=False)
    
    id_produto = models.ForeignKey('produtos.Produto',
                                    on_delete=models.DO_NOTHING,
                                    null=False,
                                    blank=False)



    def __str__(self):
        return f'Pedido {self.id} - Produto {self.id_produto.nome}'