import requests
import psycopg2

BASE_URL = "http://127.0.0.1:8000/usuarios"

def create_usuario(nome, senha):
    try:
        response = requests.post(f"{BASE_URL}/usuario/", 
        json={"nome": nome,
              "apelido": nome,
               "senha": senha,
               "cargo": "Funcionario",})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao criar usuario: {e}")
        return None

def get_usuarios():
    try:
        response = requests.get(f"{BASE_URL}/usuario/")
        response.raise_for_status()
        return response.json() 
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar usuarios: {e}")
        return []


def delete_usuario(usuario_id):
    try:
        response = requests.delete(f"{BASE_URL}/usuario/{usuario_id}")
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Erro ao deletar usuario: {e}")
        return False