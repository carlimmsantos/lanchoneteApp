from ninja import Router
from ninja import ModelSchema, Schema
from .models import Pedido
from django.http import JsonResponse
from typing import Optional, List
from django.shortcuts import get_object_or_404
from apps.relatorios.models import Relatorio


relatorio_router = Router()

class RelatorioSchema(ModelSchema):
    class Config:
        model = Relatorio
        model_fields = ['id', 'numero_mesa', 'data_hora', 'valor_total', 'quantidade_pedidos'] 
    

@relatorio_router.post('/relatorio/', response=RelatorioSchema)
def post_relatorio(request, relatorio_data: RelatorioSchema):
    
    novo_relatorio = Relatorio(
        numero_mesa = relatorio_data.numero_mesa, 
        data_hora = relatorio_data.data_hora,
        valor_total = relatorio_data.valor_total,
        quantidade_pedidos = relatorio_data.quantidade_pedidos
    )
    novo_relatorio.save()
    return novo_relatorio

@relatorio_router.get('/relatorio/', response=List[RelatorioSchema])
def get_relatorios(request):
    return Relatorio.objects.all()


@relatorio_router.get('/relatorio/{id}/', response=RelatorioSchema)
def get_relatorio(request, id: int):
    return get_object_or_404(Relatorio, pk=id)

@relatorio_router.put('/relatorio/{id}/', response=RelatorioSchema)
def update_relatorio(request, id: int, relatorio_data: RelatorioSchema):

    relatorio = get_object_or_404(Relatorio, pk=id)

    relatorio.numero_mesa = relatorio_data.numero_mesa
    relatorio.data_hora = relatorio_data.data_hora
    relatorio.valor_total = relatorio_data.valor_total
    relatorio.quantidade_pedidos = relatorio_data.quantidade_pedidos
    
    relatorio.save()

    return relatorio

@relatorio_router.delete('/relatorio/{id}/')
def delete_relatorio(request, id: int):
    relatorio = get_object_or_404(Relatorio, pk=id)
    relatorio.delete()
    return {"message": "Relatório deleted successfully"}