import flet as ft
import requests
from utils import get_categoria, get_id_categoria, get_produtos

def main(page: ft.Page):
    page.title = "Cadastro de Produtos"
    

    lista_produtos = ft.ListView()

    def preenche_lista_produtos(nome=None):
        lista_produtos.controls.clear()
        produtos = get_produtos(nome)
        for produto in produtos:
            lista_produtos.controls.append(
                ft.Container(
                    ft.Text(produto['nome']),
                    bgcolor=ft.Colors.BLACK12,
                    padding=15,
                    alignment=ft.alignment.center,
                    margin=3,
                    border_radius=10,
                )
            )
        page.update()

    def cadastrar(e):
        data = {
            "nome": produto.value,
            "preco": preco.value,
            "categoria_id": get_id_categoria(categoria.value),
        }
        try:
            response = requests.post(f"http://127.0.0.1:8000/produtos/produto/", json=data)
            if response.status_code == 200:
                lista_produtos.controls.append(
                    ft.Container(
                        ft.Text(produto.value),
                        bgcolor=ft.Colors.BLACK12,
                        padding=15,
                        alignment=ft.alignment.center,
                        margin=3,
                        border_radius=10,
                    )
                )
                produto.value = ""
                preco.value = "0"
                categoria.value = None
                page.update()
            else:
                print("Erro ao cadastrar produto:", response.text)
        except requests.exceptions.RequestException as e:
            print(f"Erro ao cadastrar produto: {e}")

    def apagar_produto(e):
        
        response = requests.delete(f"http://127.0.0.1:8000/produtos/produto/{13}")

    def editar_produto(e):

        response = requests.put(f"http://127.0.0.1:8000/")


    def filtrar(e):
        preenche_lista_produtos(produto_filtrar.value)

    # Componentes da interface
    txt_titulo = ft.Text("Título do Produto:")
    produto = ft.TextField(label="Digite o título do produto...")
    txt_preco = ft.Text("Preço do Produto:")
    preco = ft.TextField(value="0", text_align=ft.TextAlign.LEFT)
    txt_categoria = ft.Text("Categoria do Produto:")
    categoria = ft.Dropdown(
        options=[ft.dropdown.Option(i['nome']) for i in get_categoria()]
    )
    btn_produto = ft.ElevatedButton("Cadastrar Produto", on_click=cadastrar)

    btn_del_prod = ft.ElevatedButton("Apagar Produto", on_click=apagar_produto)

    btn_edit_prod = ft.ElevatedButton("Editar Produto", on_click=editar_produto)


    # Adicionando componentes à página
    page.add(
        txt_titulo,
        produto,
        txt_preco,
        preco,
        txt_categoria,
        categoria,
        btn_produto,
        btn_del_prod,
        btn_edit_prod,
    )

    # Filtro de produtos
    txt_produto_filtrar = ft.Text("Filtrar Produto:")
    produto_filtrar = ft.TextField(label="Digite o título do produto...")
    btn_filtrar = ft.IconButton(ft.Icons.FILTER_ALT, on_click=filtrar)

    page.add(
        txt_produto_filtrar,
        ft.Row([produto_filtrar, btn_filtrar]),
        lista_produtos,
    )

    # Preencher lista inicial de produtos
    preenche_lista_produtos()


    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Home"),
            ft.NavigationBarDestination(icon=ft.Icons.FOLDER, label="Produto"),
            ft.NavigationBarDestination(
                icon=ft.Icons.BOOKMARK_BORDER,
                selected_icon=ft.Icons.BOOKMARK,
                label="Administrador",
            ),
        ]
    )
    page.add(ft.Text("Body!"))


ft.app(target=main)
