import flet as ft
from utils.mesas import get_mesas, create_mesa, delete_mesa
from utils.pedidos import create_pedido

class App(ft.Column):
    def __init__(self):
        super().__init__()

def main(page: ft.Page):
    # Configurações da página
    page.title = "Restaurante Bom Sabor"
    page.window.width = 400
    page.window.height = 600
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
                        ft.Text("FATURAMENTO DO DIA: R$ ", size=14, weight=ft.FontWeight.BOLD, color="black"),
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
   

    # Criar um fundo com uma imagem
    fundo = ft.Container(
        width=400,
        height=800,
        content=ft.Image(
            src="image/background.png",  # Substitua pelo caminho da sua imagem
            fit=ft.ImageFit.COVER,  # Ajusta a imagem para cobrir toda a tela
        )
    )

    # Função para adicionar uma nova mesa
    def adicionar_mesa():
        numero_nova_mesa = len(get_mesas()) + 1
        if create_mesa(numero_nova_mesa):
            atualizar_lista_mesas()
            print(f"Mesa {numero_nova_mesa} criada com sucesso!")
        else:
            print("Erro ao criar a mesa.")

    # Botão para adicionar mesa
    button_add = ft.ElevatedButton(
        text="Adicionar Mesa",
        bgcolor="green",
        color="white",
        on_click=lambda e: adicionar_mesa(),
    )

    button_add_container = ft.Row(
        controls=[button_add],
        alignment=ft.MainAxisAlignment.END,
    )

   

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

    # Lista de mesas
    mesa_list = ft.Column(
        scroll=ft.ScrollMode.ALWAYS,  # Ativa o scroll
        expand=True,  # Permite que o conteúdo ocupe o espaço disponível
        spacing=10,
    )

    atualizar_lista_mesas()

    # Define the content column as part of the conteudo container
    content = ft.Column()
    
    # Define the change_page function before using it
    def change_page(event):
        # Limpa o conteúdo atual da aba
        conteudo.content.controls.clear()

        # Verifica qual aba foi selecionada
        if event.control.selected_index == 0:  # Aba "Mesas"
            atualizar_lista_mesas()
            conteudo.content.controls.append(
                button_add_container
            ),
            
            conteudo.content.controls.append(
                ft.Container(
                    content=mesa_list,  # Adiciona a lista de mesas com scroll
                    expand=True,  # Expande para ocupar o espaço disponível
                ),
            )

        elif event.control.selected_index == 1:  # Aba "Produtos"
            conteudo.content.controls.append(
                ft.Text("Produtos", size=18)
            )
        elif event.control.selected_index == 2:  # Aba "Administração"
            conteudo.content.controls.append(
                ft.Text("Administração", size=18)
            )

        # Atualiza a página para refletir as mudanças
        page.update()

    # Barra de navegação
    nav_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.EXPLORE,
                label="Mesa",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.COMMUTE,
                label="Produtos",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.BOOKMARK_BORDER,
                label="Gerenciamento",
            ),
        ],
        on_change=change_page,  # Conecta a função change_page
    )

    # Criar uma camada por cima da imagem
    conteudo = ft.Container(
        alignment=ft.alignment.top_center,
        content=ft.Column(
            controls=[
                button_add_container,
                ft.Container(
                    content=mesa_list,  # Adiciona a lista de mesas com scroll
                    expand=True,  # Expande para ocupar o espaço disponível
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
            nav_bar,  # Barra de navegação fixa no rodapé
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        expand=True,
    )

    # Usar um Stack para colocar a imagem no fundo e os elementos na frente
    
    app = App()
    content.controls.append(app)  
    
    page.add(ft.Stack([
        fundo, 
        #criar_header(), # Imagem de fundo
        layout_principal,  # Layout principal com conteúdo e barra de navegação
    ], expand=True))

ft.app(target=main)
