import requests


BASE_URL = "http://127.0.0.1:8000/relatorios"

def get_relatorios():
    try:
        response = requests.get(f"{BASE_URL}/relatorio/")
        response.raise_for_status()
        return response.json() 
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar relatorios: {e}")
        return []
    

def get_relatorio(relatorio_id):
    try:
        response = requests.get(f"{BASE_URL}/relatorio/{relatorio_id}")
        response.raise_for_status()
        return response.json() 
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar relatorio: {e}")
        return None

def create_relatorio(numero_mesa, tipo_desconto, tipo_pagamento, desconto, valor_total, quantidade_pedidos):
    try:
        import json

        response = requests.post(
            f"{BASE_URL}/relatorio/",
            json={
                "numero_mesa": numero_mesa,
                "tipo_desconto": tipo_desconto,
                "tipo_pagamento": tipo_pagamento,
                "desconto": desconto,
                "valor_total": valor_total,
                "quantidade_pedidos": quantidade_pedidos,
            }
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao criar relatório: {e}")
        return None