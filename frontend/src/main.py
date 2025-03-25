import flet as ft
from utils import get_mesas, delete_mesa, create_mesa

def main(page: ft.Page):
    # Configurações da página
    page.title = "Restaurante Bom Sabor"
    page.bgcolor = "#FFF5E1"
    page.window.width = 400
    page.window.height = 800
    page.window.fullscreen = False
    page.window.resizable = False
    page.padding = 10

    # Função para adicionar uma nova mesa
    def adicionar_mesa():
        numero_nova_mesa = len(get_mesas()) + 1  # Define o número da nova mesa
        if create_mesa(numero_nova_mesa):  # Chama a função para criar a mesa no backend
            atualizar_lista_mesas()  # Atualiza a lista de mesas na interface
            print(f"Mesa {numero_nova_mesa} criada com sucesso!")
        else:
            print("Erro ao criar a mesa.")

    # Botão para adicionar mesa
    button_add = ft.ElevatedButton(
        text="Adicionar Mesa",
        bgcolor="green",  # Define a cor de fundo do botão como verde
        color="white",  # Define a cor do texto como branco
        on_click=lambda e: adicionar_mesa(),  # Chama a função para criar a mesa
    )

    button_add_container = ft.Row(
        controls=[button_add],
        alignment=ft.MainAxisAlignment.END,  # Alinha o botão à direita
    )

    # Cabeçalho com logo e informações
    def criar_header():
        return ft.Container(
            content=ft.Row([
                ft.Image(
                    src="image/Icon.png",  # Caminho da imagem
                    fit=ft.ImageFit.COVER,
                    width=100,
                    height=100,
                    border_radius=5,
                ),
                ft.Column([
                    ft.Text("FATURAMENTO DO DIA: R$ 3.500,00", size=14, weight=ft.FontWeight.BOLD),
                    ft.Text("Mesas Disponíveis: 5", size=12),
                ], spacing=5)
            ], alignment=ft.MainAxisAlignment.CENTER),
            padding=10,
            border_radius=10,
            bgcolor="white",
            width=400,
        )

    # Função para atualizar a lista de mesas
    def atualizar_lista_mesas():
        mesa_list.controls.clear()  # Limpa os controles existentes
        lista_mesas = get_mesas()  # Obtém a lista atualizada do backend
        for mesa in lista_mesas:
            mesa_component = ft.Container(
                content=ft.ListTile(
                    title=ft.Text(f"Numero: {mesa['numero']}", size=16, weight=ft.FontWeight.BOLD),
                    subtitle=ft.Text(f"Disponivel: {mesa['status']}", size=12, color="black"),
                    trailing=ft.PopupMenuButton(
                        key=mesa['id'],
                        icon=ft.icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(
                                text="Editar",
                                icon=ft.icons.EDIT,
                                on_click=lambda e: print("Editar")
                            ),
                            ft.PopupMenuItem(
                                text="Excluir",
                                icon=ft.icons.DELETE,
                                on_click=lambda e, mesa_id=mesa['id']: excluir_mesa(mesa_id)
                            ),
                            ft.PopupMenuItem(
                                text="Adicionar Pedido",
                                icon=ft.icons.ADD,
                                on_click=lambda e, mesa_id=mesa['id']: print(f"Adicionar Pedido para Mesa {mesa_id}")
                            ),
                        ]
                    )
                ),
                padding=10,  # Espaçamento interno
                margin=5,  # Espaçamento externo
                border_radius=10,  # Bordas arredondadas
                bgcolor="white",  # Fundo branco
                border=ft.border.all(1, "black"),  # Borda preta de 1px
                shadow=ft.BoxShadow(
                    spread_radius=2,
                    blur_radius=5,
                    color=ft.colors.BLACK12,
                ),  # Sombra para destacar a caixa
            )
            mesa_list.controls.append(mesa_component)
        page.update()  # Atualiza a interface

    # Função para excluir uma mesa
    def excluir_mesa(mesa_id):
        if delete_mesa(mesa_id):  
            atualizar_lista_mesas()  

    # Lista de mesas
    mesa_list = ft.Column(
        scroll=ft.ScrollMode.ALWAYS,
        expand=True,
    )

    atualizar_lista_mesas()  # Renderiza a lista inicial de mesas

    # Barra de navegação
    nav_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.icons.EXPLORE,
                label="Mesa",
            ),
            ft.NavigationBarDestination(
                icon=ft.icons.COMMUTE,
                label="Produtos",
            ),
            ft.NavigationBarDestination(
                icon=ft.icons.BOOKMARK_BORDER,
                label="Gerenciamento",
            ),
        ],
    )

    # Adiciona os elementos à página
    page.add(
        criar_header(),
        button_add_container,
        mesa_list,
        nav_bar,
    )

ft.app(target=main)