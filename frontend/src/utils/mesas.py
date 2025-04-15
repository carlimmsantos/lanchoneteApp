
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

def atualizar_mesa(mesa_id, numero, status):
    try:
        response = requests.put(f"{BASE_URL}/mesa/{mesa_id}/", json={"numero": numero , "status": status})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao atualizar mesa: {e}")
        return None


def atualizar_status_mesa(mesa_id, numero):
    try:
        
        conn = psycopg2.connect(
            dbname="Gerencia",
            user="postgres",
            password="santos2018", 
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        
        
        cursor.execute("SELECT verificar_pedidos_mesa(%s);", (mesa_id,))
        resultado = cursor.fetchone()[0]  
        

        
        novo_status = not resultado  # Se houver pedidos (True), status será False; caso contrário, True

        print(f"[atualizar_status_mesa] Mesa {mesa_id} tem pedidos: {resultado}. Atualizando status para {'Disponível' if novo_status else 'Ocupado'}.")
        response = atualizar_mesa(mesa_id, numero=numero, status=novo_status)

        if response:
            print(f"[atualizar_status_mesa] Status da mesa {mesa_id} atualizado para {'Disponível' if novo_status else 'Ocupado'}.")
            return True
        else:
            print(f"[atualizar_status_mesa] Falha ao atualizar o status da mesa {mesa_id}.")
            return False

    except psycopg2.Error as e:
        print(f"[atualizar_status_mesa] Erro ao acessar o banco de dados: {e}")
        return False

    finally:
        # Fecha o cursor e a conexão
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
  