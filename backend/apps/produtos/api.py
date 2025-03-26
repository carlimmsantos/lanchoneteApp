from ninja import Router
from ninja import ModelSchema, Schema
from .models import Produto, Categoria
from django.http import JsonResponse
from typing import Optional, List
from django.shortcuts import get_object_or_404

produtos_router = Router()

class ProdutoSchema(ModelSchema):
    class Meta:
        model = Produto
        fields = ['id', 'nome', 'preco', 'categoria']

class CategoriaSchema(ModelSchema):
    class Meta:
        model = Categoria
        fields = '__all__'

@produtos_router.post('/produto/', response=ProdutoSchema)
def post_produto(request, produto: ProdutoSchema):
    produto = Produto(
        nome=produto.nome,
        preco=produto.preco,
        categoria_id=produto.categoria
    )
    produto.save()
    return produto

@produtos_router.get('/produto/', response=List[ProdutoSchema])
def get_produto(request, nome: str = None):
    produtos_list = Produto.objects.all()

    if nome:
        produtos_list = produtos_list.filter(nome__icontains=nome)

    return produtos_list

@produtos_router.get('/produto/{id_produto}', response=ProdutoSchema)
def get_produto_by_id(request, id_produto: int):
    produto = get_object_or_404(Produto, id=id_produto)
    return produto

@produtos_router.put('/produto/{id_produto}', response=ProdutoSchema)
def update_produto(request, id_produto: int, data: ProdutoSchema):
    produto = get_object_or_404(Produto, id=id_produto)
    produto.nome = data.nome
    produto.preco = data.preco
    produto.categoria = data.categoria

    produto.save()
    return produto

@produtos_router.delete('/produto/{id_produto}', response={ 200: dict})
def delete_produto(request, id_produto: int):
    try:
        produto = Produto.objects.get(id=id_produto)
        produto.delete()
        return JsonResponse({"message": "Produto deletado com sucesso!"})
    except Produto.DoesNotExist:
        return JsonResponse({"message": "Produto não encontrado!"})
    
@produtos_router.get('/categorias/', response=List[CategoriaSchema])
def get_categoria(request):
    categoria = Categoria.objects.all()
    return categoria