from ninja import NinjaAPI
from apps.produtos.api import produtos_router
from apps.mesas.api import mesa_router
from apps.pedidos.api import pedidos_router
from apps.relatorios.api import relatorio_router
from apps.usuarios.api import usuario_router

api = NinjaAPI()

api.add_router('/produtos/', produtos_router, tags=['produtos'])
api.add_router('/mesas/', mesa_router, tags=['mesas'])
api.add_router('/pedidos/', pedidos_router, tags=['pedidos'])
api.add_router('/relatorios/',relatorio_router , tags=['relatorios'])
api.add_router('/usuarios/', usuario_router, tags=['usuarios'])



