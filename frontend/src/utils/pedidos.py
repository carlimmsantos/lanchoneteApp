import requests
import psycopg2

BASE_URL = "http://127.0.0.1:8000/pedidos"


# Funções para interagir com a API de pedidos

def create_pedido(quantidade, mesa, id_produto):
    print(quantidade, mesa, id_produto)
    try:
        response = requests.post(f"{BASE_URL}/pedido/", json={ "quantidade": quantidade, "mesa_id": mesa, "id_produto_id": id_produto})
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"{quantidade}, {mesa}, {id_produto}")
        print(f"Erro ao criar pedido: {e}")
        return None

def update_pedido(pedido_id, quantidade, mesa, id_produto):
    try:
        response = requests.put(f"{BASE_URL}/pedido/{pedido_id}/", json={"quantidade": quantidade, "mesa_id": mesa, "id_produto_id": id_produto})
        print(f"{quantidade}, {mesa}, {id_produto}")
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Erro ao atualizar pedido: {e}")
        return None

def get_pedidos_por_mesa(mesa_id):
    try:
        
        conn = psycopg2.connect(
            dbname="Gerencia",
            user="postgres",
            password="suasenha",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        
        cursor.execute("SELECT * FROM get_pedidos_por_mesa(%s);", (mesa_id,))
        pedidos = cursor.fetchall()

        
        cursor.close()
        conn.close()

        
        return [
            {"pedido_id": row[0], "quantidade": row[1], "produto_nome": row[2]}
            for row in pedidos
        ]
    except Exception as e:
        print(f"Erro ao buscar pedidos: {e}")
        return []

def delete_pedido(pedido_id):
    try:
        response = requests.delete(f"{BASE_URL}/pedido/{pedido_id}/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao deletar pedido: {e}")
        return None


def apagar_pedidos_mesa(mesa_id):
    try:
        
        conn = psycopg2.connect(
            dbname="Gerencia",
            user="postgres",
            password="suasenha",
            host="localhost",
            port="5432"
        )
        
        cursor = conn.cursor()

       
        cursor.execute("CALL public.apagar_pedidos_mesa(%s);", (mesa_id,))

       
        conn.commit()

        print(f"Mesa {mesa_id} fechada com sucesso.")

    except Exception as e:
        
        print(f"Erro ao fechar a mesa {mesa_id}: {e}")

    finally:
        
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
    