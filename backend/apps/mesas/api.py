from ninja import Router
from ninja import ModelSchema, Schema
from typing import List
from .models import Mesa
from django.shortcuts import get_object_or_404

mesa_router = Router()

class MesaSchema(ModelSchema):
    class Meta:
        model = Mesa
        fields = ['numero', 'status',]

@mesa_router.post('/mesa/', response=MesaSchema)
def post_mesa(request, mesa: MesaSchema):
   
    mesa = Mesa(
        numero=mesa.numero,
        status=mesa.status,
    )
    
    mesa.save()
    return mesa

@mesa_router.get('/mesa/', response=List[MesaSchema])
def get_mesa(request, numero: int = None):
    mesa_list = Mesa.objects.all()

    if numero:
        mesa_list = mesa_list.filter(numero__icontains=numero)

    return mesa_list

@mesa_router.get('/mesa/{id_mesa}', response=MesaSchema)
def get_mesa_by_id(request, id_mesa: int):
    mesa = get_object_or_404(Mesa, id=id_mesa)
    return mesa

@mesa_router.put('/mesa/{id_mesa}', response=MesaSchema)
def update_mesa(request, id_mesa: int, data: MesaSchema):
    mesa = get_object_or_404(Mesa, id=id_mesa)
    for attr, value in data.dict().items():
        setattr(mesa, attr, value)
    mesa.save()
    return mesa

@mesa_router.delete('/mesa/{id_mesa}', response={ 'success': bool })
def delete_mesa(request, id_mesa: int):
    mesa = get_object_or_404(Mesa, id=id_mesa)
    mesa.delete()
    return { 'success': True }