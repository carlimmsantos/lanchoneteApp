from ninja import Router
from ninja import ModelSchema, Schema
from django.http import JsonResponse
from typing import Optional, List
from django.shortcuts import get_object_or_404
from apps.usuarios.models import Usuario

usuario_router = Router()

class UsuarioSchema(ModelSchema):
    class Config:
        model = Usuario
        model_fields = ["id",'nome', 'apelido', 'senha', 'cargo']


@usuario_router.post('/usuario/', response=UsuarioSchema)
def post_usuario(request, usuario_data: UsuarioSchema):
    novo_usuario = Usuario(
        nome=usuario_data.nome,
        apelido=usuario_data.apelido,
        senha=usuario_data.senha,
        cargo=usuario_data.cargo
    )
    novo_usuario.save()
    return novo_usuario

@usuario_router.get('/usuario/', response=List[UsuarioSchema])
def get_usuarios(request):
    return Usuario.objects.all()

@usuario_router.get('/usuario/{id}/', response=UsuarioSchema)
def get_usuario(request, id: int):
    return get_object_or_404(Usuario, pk=id)

@usuario_router.put('/usuario/{id}/', response=UsuarioSchema)
def update_usuario(request, id: int, usuario_data: UsuarioSchema):
    usuario = get_object_or_404(Usuario, pk=id)

    usuario.nome = usuario_data.nome
    usuario.apelido = usuario_data.apelido
    usuario.senha = usuario_data.senha
    usuario.cargo = usuario_data.cargo
    
    usuario.save()

    return usuario

@usuario_router.delete('/usuario/{id}/')
def delete_usuario(request, id: int):
    usuario = get_object_or_404(Usuario, pk=id)
    usuario.delete()
    return JsonResponse({'success': True})