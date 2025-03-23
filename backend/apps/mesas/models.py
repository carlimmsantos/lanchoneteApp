from django.db import models

# Create your models here.

class Mesa(models.Model):
    numero = models.IntegerField()
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Mesa {self.numero}'