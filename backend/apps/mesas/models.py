from django.db import models


class Mesa(models.Model):
    id = models.AutoField(primary_key=True)
    numero = models.IntegerField()
    status = models.BooleanField(default=True)
   
    def __str__(self):
        return f"{self.id}"
