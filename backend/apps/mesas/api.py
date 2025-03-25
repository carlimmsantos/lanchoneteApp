from ninja import Router
from ninja import ModelSchema, Schema
from typing import List
from .models import Mesa
from django.shortcuts import get_object_or_404

mesa_router = Router()

class MesaSchema(ModelSchema):
    class Meta:
        model = Mesa
        fields = ['id','numero', 'status', 'id_pedido']

@mesa_router.post('/mesa/', response=MesaSchema)
def post_mesa(request, mesa: MesaSchema):
    mesa = Mesa(
        id=mesa.id,
        numero=mesa.numero,
        status=mesa.status,
        id_pedido=mesa.id_pedido
    )
    mesa.save()
    return mesa

@mesa_router.get('/mesa/', response=List[MesaSchema])
def get_mesas(request):
    return Mesa.objects.all()

@mesa_router.get('/mesa/{id}/', response=MesaSchema)
def get_mesa(request, id: int):
    return get_object_or_404(Mesa, pk=id)

@mesa_router.put('/mesa/{id}/', response=MesaSchema)
def put_mesa(request, id: int, mesa: MesaSchema):
    mesa = get_object_or_404(Mesa, pk=id)
    mesa.numero = mesa.numero
    mesa.status = mesa.status
    mesa.id_pedido = mesa.id_pedido
    mesa.save()
    return mesa

@mesa_router.delete('/mesa/{id}/')
def delete_mesa(request, id: int):
    mesa = get_object_or_404(Mesa, pk=id)
    mesa.delete()
    return {"message": "Mesa deleted successfully"}