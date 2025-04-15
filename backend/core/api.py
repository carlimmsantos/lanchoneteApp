from ninja import NinjaAPI
from apps.produtos.api import produtos_router
from apps.mesas.api import mesa_router
from apps.pedidos.api import pedidos_router

api = NinjaAPI()

api.add_router('/produtos/', produtos_router, tags=['produtos'])
api.add_router('/mesas/', mesa_router, tags=['mesas'])
api.add_router('/pedidos/', pedidos_router, tags=['pedidos'])
api.add_router('/relatorios/', produtos_router, tags=['relatorios'])



