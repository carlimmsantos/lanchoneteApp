import flet as ft
import requests

def get_categoria():
    response = requests.get('http://127.0.0.1:8000/produtos/categorias/')
    return response.json()


def main(page: ft.Page):
    page.title = 'Cadastro de Produtos' 

    lista_produtos = ft.ListView()

    def cadatrar(e):
        data = {
            "nome": produto.value,
            "preco": preco.value,
            "categoria_id": 1
        }

        response = requests.post('http://127.0.0.1:8000/produtos/produto/', json=data)

        if response.status_code == 200:
            lista_produtos.controls.append(
                ft.Container(

                    ft.Text(produto.value),
                    bgcolor= ft.colors.BLACK12,
                    padding=15,
                    alignment=ft.Alignment.CENTER,
                    margin=3,
                    border_radius=10,
                    )
            
            )
        page.update()


    txt_titulo = ft.Text('Titulo do Produto: ')
    produto = ft.TextField(label='Digite o titulo do produto..',)
    txt_preco = ft.Text('Preço do Produto: ')
    preco = ft.TextField(value="0", label='Digite o preço do produto..',text_align=ft.TextAlign.LEFT)
    
    txt_categoria = ft.Text('Categoria do Produto: ')
    categoria = ft.Dropdown(
        options=[
            ft.dropdown.Option(i['nome']) for i in get_categoria()
        ]
    )

    btn_produto = ft.ElevatedButton('Cadastrar Produto', on_click=cadatrar)

    page.add(
       
        txt_titulo,
        produto,
        txt_preco,
        preco,
        txt_categoria,
        categoria,
        btn_produto,
        
        )
    
    
    
    page.add(
         
         lista_produtos
         )
    

ft.app(target=main)
