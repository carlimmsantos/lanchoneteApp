from ninja import Router
from ninja import ModelSchema, Schema
from .models import Pedido
from django.http import JsonResponse
from typing import Optional, List
from django.shortcuts import get_object_or_404
from apps.mesas.models import Mesa

pedidos_router = Router()

class PedidoSchema(ModelSchema):
    class Meta:
        model = Pedido
        fields = ['id', 'quantidade', 'mesa', 'id_produto']


@pedidos_router.post('/pedido/', response=PedidoSchema)
def post_pedido(request, pedido: PedidoSchema):
    
    novo_pedido = Pedido(
        quantidade=pedido.quantidade, 
        mesa_id=pedido.mesa,
        id_produto_id=pedido.id_produto  
    )
    novo_pedido.save()
    return novo_pedido


@pedidos_router.get('/pedido/', response=List[PedidoSchema])
def get_pedidos(request):
    return Pedido.objects.all()

@pedidos_router.get('/pedido/{id}/', response=PedidoSchema)
def get_pedido(request, id: int):
    return get_object_or_404(Pedido, pk=id)

@pedidos_router.put('/pedido/{id}/', response=PedidoSchema)
def put_pedido(request, id: int, pedido: PedidoSchema):
    pedido = get_object_or_404(Pedido, pk=id)
    pedido.quantidade = pedido.quantidade
    pedido.id_produto = pedido.id_produto
    pedido.save()
    return pedido

@pedidos_router.delete('/pedido/{id}/')
def delete_pedido(request, id: int):
    pedido = get_object_or_404(Pedido, pk=id)
    pedido.delete()
    return {"message": "Pedido deleted successfully"}