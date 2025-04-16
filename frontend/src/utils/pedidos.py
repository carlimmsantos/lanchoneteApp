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
        # Conexão com o banco de dados
        conn = psycopg2.connect(
            dbname="gerencia",
            user="postgres",
            password="0121",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        # Chamada da função no banco de dados
        cursor.execute("SELECT * FROM get_pedidos_por_mesa(%s);", (mesa_id,))
        pedidos = cursor.fetchall()

        # Fechar conexão
        cursor.close()
        conn.close()

        # Retornar os pedidos
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
        # Conexão com o banco de dados
        conn = psycopg2.connect(
            dbname="gerencia",
            user="postgres",
            password="0121",
            host="localhost",
            port="5432"
        )
        # Criação de um cursor para executar comandos SQL
        cursor = conn.cursor()

        # Chamada do procedimento armazenado
        cursor.execute("CALL public.apagar_pedidos_mesa(%s);", (mesa_id,))

        # Confirma a transação
        conn.commit()

        print(f"Mesa {mesa_id} fechada com sucesso.")

    except Exception as e:
        # Tratamento de erros
        print(f"Erro ao fechar a mesa {mesa_id}: {e}")

    finally:
        # Fecha o cursor e a conexão
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
    