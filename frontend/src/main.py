import flet as ft
from utils.mesas import get_mesas, create_mesa, delete_mesa
from utils.produtos import get_produtos, create_produto, delete_produto, update_produto
from utils.pedidos import create_pedido

class App(ft.Column):
    def __init__(self):
        super().__init__()

def main(page: ft.Page):
    # Configurações da página
    page.title = "Restaurante Bom Sabor"
    page.window.width = 400
    page.window.height = 800
    page.window.fullscreen = False
    page.window.resizable = False

    # Cabeçalho com logo e informações
    def criar_header():
        return ft.Container(
            content=ft.Row([
                
                ft.Image(
                    src="image/Icon.png",
                    fit=ft.ImageFit.COVER,
                    width=100,
                    height=100,
                    border_radius=5,
                ),

                ft.Column(
                    [
                        ft.Text("Usuario: Admin", size=14, weight=ft.FontWeight.BOLD, color="black"),
                        ft.Text(f"Mesas Disponíveis: {len(get_mesas())}", size=12, color="black"),
                    ], 
                    spacing=5)
            ], 


           
            alignment=ft.MainAxisAlignment.START),
            padding=10,
            border_radius=20,
            bgcolor="white", 
            width=400,
            border=ft.border.all(1, "black"),
            margin=5,

        )
   
    #FUNÇÕES MESAS

    # Função para adicionar uma nova mesa
    def adicionar_mesa():
        numero_nova_mesa = len(get_mesas()) + 1
        if create_mesa(numero_nova_mesa):
            atualizar_lista_mesas()
            print(f"Mesa {numero_nova_mesa} criada com sucesso!")
        else:
            print("Erro ao criar a mesa.")

    # Função para atualizar a lista de mesas
    def atualizar_lista_mesas():
        mesa_list.controls.clear()
        lista_mesas = get_mesas()
        for mesa in lista_mesas:
            mesa_component = ft.Container(
                content=ft.ListTile(

                    #title=ft.Text(f"Mesa {mesa['numero']:02d}", size=16, weight=ft.FontWeight.BOLD, color='black'),
                    #subtitle=ft.Text(f"Disponível: {mesa['status']}", size=12, color="black"),
                    
                    title=ft.Row(
                                controls=[
                                    ft.Text(
                                        f"Mesa {mesa['numero']:02d}",
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        color="black"
                                    ),
                                    ft.Text(
                                        f"{'Disponível' if mesa['status'] else 'Indisponivel'}",
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        color="green" if mesa['status'] else "red"  
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=20,
                                height=60,
                            ),


                    trailing=ft.PopupMenuButton(
                        key=mesa['id'],
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(
                                text="Editar",
                                icon=ft.Icons.EDIT,
                                on_click=lambda e: print("Editar")
                            ),
                            ft.PopupMenuItem(
                                text="Excluir",
                                icon=ft.Icons.DELETE,
                                on_click=lambda e, mesa_id=mesa['id']: excluir_mesa(mesa_id)
                            ),
                            ft.PopupMenuItem(
                                text="Adicionar Pedido",
                                icon=ft.Icons.ADD,
                                on_click=lambda e, mesa_id=mesa['id']: create_pedido(1,mesa_id,1)
                            ),
                            
                        ]
                     
                    )
                ),
                padding=10,
                margin=5,
                border_radius=10,
                bgcolor= "white", 
                border=ft.border.all(1, "black"),
            )
            mesa_list.controls.append(mesa_component)
        page.update()

    # Função para excluir uma mesa
    def excluir_mesa(mesa_id):
        if delete_mesa(mesa_id):  
            atualizar_lista_mesas()  

    
    #FUNÇÕES PRODUTOS


    # Função para adicionar um novo produto
    def adicionar_produto(nome, preco):
        try:
            preco = float(preco)  # Certifique-se de que o preço é um número
            if create_produto(nome, preco):
                print(f"Produto {nome} criado com sucesso!")
                atualizar_lista_produtos()
            else:
                print("Erro ao criar o produto.")
        except ValueError:
            print("Erro: O preço deve ser um número válido.")

    # Função para atualizar a lista de produtos
    def atualizar_lista_produtos():
        produto_list.controls.clear()
        lista_produtos = get_produtos()
        for produto in lista_produtos:
            produto_component = ft.Container(
                content=ft.ListTile(
                    title=ft.Text(produto['nome'], size=16, weight=ft.FontWeight.BOLD, color='black'),
                    subtitle=ft.Text(f"R$ {produto['preco']:.2f}", size=12, color="black"),
                    trailing=ft.PopupMenuButton(
                        key=produto['id'],
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(
                                text="Editar",
                                icon=ft.Icons.EDIT,
                                on_click=lambda e, produto_id=produto['id']: abrir_editar_produto(produto_id)
                            ),
                            ft.PopupMenuItem(
                                text="Excluir",
                                icon=ft.Icons.DELETE,
                                on_click=lambda e, produto_id=produto['id']: excluir_produto(produto_id)
                            )
                        ]
                    )
                ),
                padding=10,
                margin=5,
                border_radius=10,
                bgcolor="white",
                border=ft.border.all(1, "black"),
            )
            produto_list.controls.append(produto_component)
        page.update()

    # Função para abrir o BottomSheet de edição de produto
    def abrir_editar_produto(produto_id):
        page.id_produto_atual = produto_id

        produto = next((p for p in get_produtos() if p['id'] == produto_id), None)
    
        if produto:

            nome_field.value = produto['nome']
            preco_field.value = str(produto['preco'])
            print(produto_id)
            print(nome_field.value)
            print(preco_field.value)
            
            page.open(bs_editar)
            page.update()

    # Função para excluir um produto
    def excluir_produto(produto_id):
        print(produto_id)
        if delete_produto(produto_id):
            atualizar_lista_produtos()

    # Função para mudar de abas
    def change_page(event):
        # Limpa o conteúdo atual da aba
        conteudo.content.controls.clear()

        # Verifica qual aba foi selecionada
        if event.control.selected_index == 0: 
            atualizar_lista_mesas()
            conteudo.content.controls.append(
                button_add_container
            ),
            
            conteudo.content.controls.append(
                ft.Container(
                    content=mesa_list, 
                    expand=True,
                ),
            )

        elif event.control.selected_index == 1: 
            atualizar_lista_produtos()
            conteudo.content.controls.append(
                button_add_produto_container,
            ),
            conteudo.content.controls.append(
                ft.Container(
                    content=produto_list,
                    expand=True,
                ),
            ),
        
        elif event.control.selected_index == 2: 
            conteudo.content.controls.append(
                ft.Text("Administração Em Desenvolvimento", size=16)
            )

        # Atualiza a página para refletir as mudanças
        page.update()
    
    # Função para atualizar a lista de produtos
    def atualizar_produtos(nome, preco):
        try:
            preco = float(preco)  # Certifique-se de que o preço é um número
            id_produto = page.id_produto_atual
            print(id_produto)
            if update_produto(id_produto, nome, preco):
                print(f"Produto {nome} atualizado com sucesso!")
                atualizar_lista_produtos()
            else:
                print("Erro ao atualizar o produto.")
        except ValueError:
            print("Erro: O preço deve ser um número válido.")

    # Função para lidar com o fechamento do BottomSheet
    def handle_dismissal(e):
        page.add(ft.Text("Bottom sheet dismissed"))
    

    # Criar um fundo com uma imagem
    fundo = ft.Container(
        width=400,
        height=800,
        content=ft.Image(
            src="image/background.png",  
            fit=ft.ImageFit.COVER,  
        )
    )

    # Campos do formulário
    nome_field = ft.TextField(
        label="Nome do Produto",
        autofill_hints=ft.AutofillHint.NAME,
    )
    preco_field = ft.TextField(
        label="Preço",
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    # BottomSheet para adicionar produto
    bs = ft.BottomSheet(
        on_dismiss=handle_dismissal,
        content=ft.Container(
            padding=50,
            content=ft.Column(
                tight=True,
                controls=[
                    nome_field,
                    preco_field,
                    ft.ElevatedButton("Cadastrar Produto",
                    on_click=lambda e: adicionar_produto(nome_field.value, preco_field.value)),
                ],
            ),
        ),
    )

    # BottomSheet para editar produto
    bs_editar = ft.BottomSheet(
        on_dismiss=handle_dismissal,
        content=ft.Container(
            padding=50,
            content=ft.Column(
                tight=True,
                controls=[
                    nome_field,
                    preco_field,
                    ft.ElevatedButton("Atualizar Produto",
                    on_click=lambda e: atualizar_produtos(nome_field.value, preco_field.value)),
                ],
            ),
        ),
    )

#Botão para adicionar produto
    button_add_produto = ft.ElevatedButton(
        text="Adicionar Produto",
        bgcolor="green",
        color="white",
        on_click=lambda e: page.open(bs),
    )

    # Container para o botão de adicionar produto
    button_add_produto_container = ft.Row(
        controls=[button_add_produto],
        alignment=ft.MainAxisAlignment.END,
    )

    # Botão para adicionar mesa
    button_add = ft.ElevatedButton(
        text="Adicionar Mesa",
        bgcolor="green",
        color="white",
        on_click=lambda e: adicionar_mesa(),
    )

    # Container para o botão de adicionar mesa
    button_add_container = ft.Row(
        controls=[button_add],
        alignment=ft.MainAxisAlignment.END,
    ) 

    # Lista de mesas
    mesa_list = ft.Column(
        scroll=ft.ScrollMode.ALWAYS,  
        expand=True,
        spacing=10,
    )

    #Lista de produtos
    produto_list = ft.Column(
        scroll=ft.ScrollMode.ALWAYS,  
        expand=True,
        spacing=10,
    )

    atualizar_lista_mesas()
    atualizar_lista_produtos()

    content = ft.Column()

    # Barra de navegação
    nav_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.HOME,
                label="Mesa",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.SHOP,
                label="Produtos",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.BOOKMARK_BORDER,
                label="Gerenciamento",
                bgcolor="black",
            ),
        ],
        bgcolor="white",
        on_change=change_page, 
    )

    # Criar uma camada por cima da imagem
    conteudo = ft.Container(
        alignment=ft.alignment.top_center,
        content=ft.Column(
            controls=[
                button_add_container,
                ft.Container(
                    content=mesa_list,
                    expand=True, 
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=True,
        ),
    )
    

    # Adicionar a barra de navegação fixa no rodapé
    layout_principal = ft.Column(
        controls=[
            criar_header(),
            ft.Container(
                content=conteudo,
                expand=True,
            ),
            nav_bar,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        expand=True,
    )

    
    app = App()
    content.controls.append(app)  
    
    page.add(ft.Stack([
        fundo, 
        #criar_header(), 
        layout_principal,
    ], expand=True))

ft.app(target=main)
