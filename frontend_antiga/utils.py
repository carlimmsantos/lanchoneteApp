# filepath: c:\Users\carlo\Documents\Programação\lanchoneteApp\frontend\utils.py
import requests

BASE_URL = "http://127.0.0.1:8000/produtos"

def get_categoria():
    try:
        response = requests.get(f"{BASE_URL}/categorias/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar categorias: {e}")
        return []

def get_id_categoria(nome):
    categorias = get_categoria()
    for categoria in categorias:
        if categoria['nome'] == nome:
            return categoria['id']
    return None

def get_produtos(nome=None):
    try:
        url = f"{BASE_URL}/produto/"
        if nome:
            url += f"?nome={nome}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar produtos: {e}")
        return []
