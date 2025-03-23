from ninja import NinjaAPI
from apps.produtos.api import produtos_router
from apps.mesas.api import mesa_router

api = NinjaAPI()

api.add_router('/produtos/', produtos_router)
api.add_router('/mesas/', mesa_router)
