from django.db import models

# Create your models here.

class Pedido (models.Model):
    id = models.AutoField(primary_key=True)
    quantidade = models.IntegerField()
    id_produto = models.ForeignKey('produtos.Produto',
                                    on_delete=models.DO_NOTHING,
                                    null=False,
                                    blank=False)



    def __str__(self):
        return f'Pedido {self.id} - Produto {self.id_produto.nome}'