
import requests
import psycopg2

BASE_URL = "http://127.0.0.1:8000/mesas"


# Funções para interagir com a API de mesas

def create_mesa(numero):
    try:
        response = requests.post(f"{BASE_URL}/mesa/", json={"numero": numero})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao criar mesa: {e}")
        return None

def get_mesas():
    try:
        response = requests.get(f"{BASE_URL}/mesa/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar mesas: {e}")
        return []

def delete_mesa(mesa_id):
    try:
        response = requests.delete(f"{BASE_URL}/mesa/{mesa_id}/")
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Erro ao deletar mesa: {e}")
        return False
    


def alterar_mesa_status(mesa_id):
    try:
        
        conn = psycopg2.connect(
            dbname="Gerencia",
            user="postgres",
            password="santos2018",  
            host="localhost",
            port="5432"
        )
        
        cursor = conn.cursor()


        cursor.execute("CALL alterar_mesa_status(%s);", (mesa_id,))

        
        conn.commit()

        print(f"Status da mesa {mesa_id} atualizado com sucesso.")
        return True

    except psycopg2.Error as e:
        
        print(f"Erro ao alterar o status da mesa {mesa_id}: {e}")
        return False

    finally:
        
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()   