import requests

BASE_URL = "http://127.0.0.1:8000/pedidos"


# Funções para interagir com a API de pedidos

def create_pedido(quantidade, mesa, id_produto):
    try:
        response = requests.post(f"{BASE_URL}/pedido/", json={ "quantidade": quantidade, "mesa_id": mesa, "id_produto_id": id_produto})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"{quantidade}, {mesa}, {id_produto}")
        print(f"Erro ao criar pedido: {e}")
        return None