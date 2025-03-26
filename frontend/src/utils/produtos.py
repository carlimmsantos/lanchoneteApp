import requests

BASE_URL = "http://127.0.0.1:8000/produtos"

def create_produto(nome, preco):
    try:
        print(nome, preco)
        response = requests.post(f"{BASE_URL}/produto/", json={"nome": nome, "preco": preco, "categoria_id": 1})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao criar produto: {e}")
        return None
    
def get_produtos():
    try:
        response = requests.get(f"{BASE_URL}/produto/")
        response.raise_for_status()
        return response.json() 
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar produtos: {e}")
        return []  
    
def delete_produto(produto_id):
    try:
        response = requests.delete(f"{BASE_URL}/produto/{produto_id}")
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Erro ao deletar produto: {e}")
        return False