from django.db import models


class Mesa(models.Model):
    id = models.AutoField(primary_key=True)
    numero = models.IntegerField()
    status = models.BooleanField(default=False)
    id_pedido = models.ForeignKey("pedidos.Pedido",
                                    on_delete=models.DO_NOTHING,
                                    null=True,
                                    blank=True)

    def __str__(self):
        return f"{self.id}"
