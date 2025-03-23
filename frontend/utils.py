# filepath: c:\Users\carlo\Documents\Programação\lanchoneteApp\frontend\utils.py
import requests

def get_categoria():
    response = requests.get('http://127.0.0.1:8000/produtos/categorias/')
    response.raise_for_status()  # Levanta uma exceção para erros HTTP
    return response.json()

def get_id_categoria(nome):
    for i in get_categoria():
        if i['nome'] == nome:
            return i['id']
    return None  # Retorna None se a categoria não for encontrada


def get_produtos(nome =None):
    response = requests.get('http://127.0.0.1:8000/produtos/produto/', params={'nome': nome})
    return response.json()
