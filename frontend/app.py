import flet as ft
import requests
from utils import get_categoria, get_id_categoria, get_produtos


def main(page: ft.Page):
    page.title = 'Cadastro de Produtos' 
    

    lista_produtos = ft.ListView()

    def preenche_lista_produtos(nome=None):
        
        for i in get_produtos(nome):
            lista_produtos.controls.append(
                ft.Container(

                    ft.Text(i['nome']),
                    bgcolor= ft.colors.BLACK12,
                    padding=15,
                    alignment=ft.alignment.center,
                    margin=3,
                    border_radius=10,
                    )
            
            )


    def cadatrar(e):

        data = {
            "nome": produto.value,
            "preco": preco.value,
            "categoria_id": get_id_categoria(categoria.value)
        }

        response = requests.post('http://127.0.0.1:8000/produtos/produto/', json=data)

        if response.status_code == 200:
            lista_produtos.controls.append(
                ft.Container(

                    ft.Text(produto.value),
                    bgcolor= ft.colors.BLACK12,
                    padding=15,
                    alignment=ft.alignment.center,
                    margin=3,
                    border_radius=10,
                    )
            
            )
        page.update()

    def filtrar(e):
        lista_produtos.controls.clear()
        preenche_lista_produtos(produto_filtrar.value)
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
    
    txt_produto_filtrar = ft.Text('Filtrar Produto: ')
    produto_filtrar = ft.TextField(label='Digite o titulo do produto..',)
    btn_filtrar = ft.IconButton(ft.icons.FILTER_ALT, on_click=filtrar)
    preenche_lista_produtos()
    
    page.add(  
        txt_produto_filtrar,
        ft.Row([
            produto_filtrar,
            btn_filtrar
        ]),
        lista_produtos,
         )
    

ft.app(target=main)
