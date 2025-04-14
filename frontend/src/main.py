import flet as ft
from utils.mesas import get_mesas, create_mesa, delete_mesa, alterar_mesa_status
from utils.produtos import get_produtos, create_produto, delete_produto, update_produto
from utils.pedidos import create_pedido, get_pedidos_por_mesa, apagar_pedidos_mesa



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

    # Função para criar o cabeçalho
    def criar_header():
        return ft.Container(
            content=ft.Row(
                [
                    ft.Image(
                        src="image/Icon.png",
                        fit=ft.ImageFit.COVER,
                        width=100,
                        height=100,
                        border_radius=5,
                    ),
                    ft.Column(
                        [
                            ft.Text(
                                "Usuario: Admin",
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color="black",
                            ),
                            ft.Text(
                                f"Mesas Disponíveis: {len(get_mesas())}",
                                size=12,
                                color="black",
                            ),
                        ],
                        spacing=5,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=10,
            border_radius=20,
            bgcolor="white",
            width=400,
            border=ft.border.all(1, "black"),
            margin=5,
        )


    # Função para exibir pedidos de uma mesa
    def exibir_pedidos(mesa_id):
        pedidos = get_pedidos_por_mesa(mesa_id)

        pedidos_list.controls.clear()

        lista_produto = get_produtos() 

        valor_total = 0.0

        if pedidos:
            for pedido in pedidos:
                
                produto = next((p for p in lista_produto if pedido["produto_nome"] == p['nome']), None)
                
                if produto:
                    valor_total += pedido['quantidade'] * produto['preco']
                    
                    pedidos_list.controls.append(
                        ft.Container(
                            content=ft.ListTile(
                                title=ft.Text(f"Pedido {pedido['pedido_id']}"),
                                subtitle=ft.Text(
                                    f"{pedido['quantidade']} X {produto['nome']} = R$ {pedido['quantidade'] * produto['preco']:.2f}",
                                    size=12, color="black"
                                ),
                            ),
                            bgcolor="white",
                            padding=10,
                            margin=5,
                            border_radius=10,
                            border=ft.border.all(1, "black"),
                        )
                    )
                else:
                    pedidos_list.controls.append(
                        ft.Text(f"Produto com ID {pedido.get('produto_id')} não encontrado.")
                    )




        else:
            pedidos_list.controls.append(
                ft.Text(f"Nenhum pedido encontrado para a mesa {mesa_id}.")
            )

        page.update()

      
        fundo_pedidos = ft.Container(
            width=400,
            height=800,
            content=ft.Image(
                src="image/background.png",
                fit=ft.ImageFit.COVER,
            ),
        )

        button_close_pedido = ft.ElevatedButton(
            "Pagamentos",
            bgcolor="green",
            color="white",
            on_click=lambda e: pagamento_pedido(mesa_id),
        )

        

       
        head_pedidos = ft.Container(
            content=ft.Row(
                [
                    ft.Image(
                        src="image/Icon.png",
                        fit=ft.ImageFit.COVER,
                        width=100,
                        height=100,
                        border_radius=5,
                    ),
                    ft.Column(
                        [
                            ft.Text(
                                f"Mesa {mesa_id}",
                                size=21,
                                weight=ft.FontWeight.BOLD,
                                color="black",
                            ),
                            ft.Text(
                                f"Valor Total: R$ {valor_total:.2f}",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color="black",
                            ),


                        ],
                        spacing=10,

                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=10,
            border_radius=20,
            bgcolor="white",
            width=400,
            border=ft.border.all(1, "black"),
            margin=5,
        )

        # Camada de pedidos
        camada_pedidos = ft.Container(
            alignment=ft.alignment.top_center,
            content=ft.Column(
                controls=[
                    head_pedidos,
                    pedidos_list,
                    ft.ElevatedButton(
                        "Voltar", on_click=lambda e: voltar()
                    ),
                    button_close_pedido,
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=20,
            ),
            padding=20,
        )

        # Adiciona o plano de fundo e a camada ao Stack
        page.views.append(
            ft.View(
                "/pedidos",
                controls=[
                    ft.Stack(
                        controls=[
                            fundo_pedidos,  # Plano de fundo
                            camada_pedidos,  # Camada de conteúdo
                        ],
                        expand=True,
                    )
                ],
            )
        )
        page.overlay.append(bs_pagamento)

        page.update()

    def voltar():
        if page.views:
            page.views.pop()
            page.update()

    def atualizar_produtos_por_id():
        global produtos_por_id
        produtos_por_id = {produto['id']: produto for produto in get_produtos()}

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
                    title=ft.Row(
                        controls=[
                            ft.Text(
                                f"Mesa {mesa['numero']:02d}",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color="black",
                            ),
                            ft.Text(
                                f"{'Disponível' if mesa['status'] else 'Indisponível'}",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color="green" if mesa['status'] else "red",
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=20,
                        height=60,
                    ),
                    trailing=ft.PopupMenuButton(
                        key=mesa["id"],
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(
                                text="Editar",
                                icon=ft.Icons.EDIT,
                                on_click=lambda e: print("Editar"),
                            ),
                            ft.PopupMenuItem(
                                text="Excluir",
                                icon=ft.Icons.DELETE,
                                on_click=lambda e, mesa_id=mesa["id"]: excluir_mesa(
                                    mesa_id
                                ),
                            ),
                            ft.PopupMenuItem(
                                text="Adicionar Pedido",
                                icon=ft.Icons.ADD,
                                on_click=lambda e, mesa_id=mesa["id"]: adicionar_pedido(
                                    mesa_id
                                ),
                            ),
                            ft.PopupMenuItem(
                                text="Ver Pedidos",
                                icon=ft.Icons.LIST,
                                on_click=lambda e, mesa_id=mesa["id"]: exibir_pedidos(
                                    mesa_id
                                ),
                            ),
                        ],
                    ),
                ),
                padding=10,
                margin=5,
                border_radius=10,
                bgcolor="white",
                border=ft.border.all(1, "black"),
            )
            mesa_list.controls.append(mesa_component)
        page.update()

    # Função para excluir uma mesa
    def excluir_mesa(mesa_id):
        if delete_mesa(mesa_id):
            atualizar_lista_mesas()

    # Função para adicionar um novo produto
    def adicionar_produto(nome, preco):
        try:
            preco = float(preco)  # Certifique-se de que o preço é um número
            if create_produto(nome, preco):
                print(f"Produto {nome} criado com sucesso!")
                atualizar_lista_produtos()
                atualizar_dropdown_produtos()

                nome_field.value = ""
                preco_field.value = ""
                page.update()
                
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

        elif event.control.selected_index == 1:  # Aba "Produtos"
            atualizar_lista_produtos()  # Atualiza a lista de produtos
            conteudo.content.controls.append(
                campo_busca_produto_container,  # Adiciona o campo de busca por nome
            )
            conteudo.content.controls.append(
                campo_busca_preco_container,  # Adiciona o campo de busca por preço
            )
            conteudo.content.controls.append(
                button_add_produto_container,
            )
            conteudo.content.controls.append(
                ft.Container(
                    content=produto_list,
                    expand=True,
                ),
            )
        
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
                atualizar_dropdown_produtos()
                page.close(bs_editar)
                atualizar_produtos_por_id()
            else:
                print("Erro ao atualizar o produto.")
        except ValueError:
            print("Erro: O preço deve ser um número válido.")

    # Função para buscar o ID do produto pelo nome
    def buscar_id_produto_por_nome(nome_produto):
        lista_produtos = get_produtos()
        produto = next((p for p in lista_produtos if p['nome'] == nome_produto), None)
        if produto:
            return produto['id']
        else:
            print(f"Produto com nome '{nome_produto}' não encontrado.")
            return None
  
    #FUNÇÕES PEDIDOS
    
    def adicionar_pedido(mesa_id):
        page.open(bs_adicionar_pedido)
        page.mesa_id = mesa_id
        page.update()
        alterar_mesa_status(mesa_id)
        atualizar_lista_mesas()
        
    def atualizar_dropdown_produtos():
        lista_produtos = get_produtos()  
        add_list_produto.options = [
            ft.DropdownOption(lista_produtos[i]['nome']) for i in range(len(lista_produtos))
        ]
        page.update()  # Atualiza a página para refletir as mudanças
    
    def pagamento_pedido(mesa_id):
        page.mesa_id_pagamento = mesa_id

        print(f"Estou na {mesa_id}")

        page.open(bs_pagamento)

        page.update()


    def filtrar_produtos_por_preco(preco_maximo):
        try:
            preco_maximo = float(preco_maximo)  # Converte o valor para float
            lista_produtos = get_produtos()
            produtos_filtrados = [p for p in lista_produtos if p['preco'] <= preco_maximo]
            return produtos_filtrados
        except ValueError:
            print("Erro: O preço deve ser um número válido.")
            return [] 

    def atualizar_lista_produtos_filtrados_por_preco(preco_maximo):
        produto_list.controls.clear()  # Limpa a lista de produtos exibida
        produtos_filtrados = filtrar_produtos_por_preco(preco_maximo)  # Filtra os produtos
        for produto in produtos_filtrados:
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
            produto_list.controls.append(produto_component)  # Adiciona o produto filtrado à lista
        page.update()  # Atualiza a página para refletir as mudanças       


    def filtrar_produtos(nome_produto):
        lista_produtos = get_produtos()
        produtos_filtrados = [p for p in lista_produtos if nome_produto.lower() in p['nome'].lower()]
        return produtos_filtrados

    def filtrar_produtos_por_preco(preco_maximo):
        try:
            preco_maximo = float(preco_maximo)  # Converte o valor para float
            lista_produtos = get_produtos()
            produtos_filtrados = [p for p in lista_produtos if p['preco'] <= preco_maximo]
            return produtos_filtrados
        except ValueError:
            print("Erro: O preço deve ser um número válido.")
            return []
        
    def atualizar_lista_produtos_filtrados(nome_produto):
        produto_list.controls.clear()  # Limpa a lista de produtos exibida
        produtos_filtrados = filtrar_produtos(nome_produto)  # Filtra os produtos
        for produto in produtos_filtrados:
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
            produto_list.controls.append(produto_component)  # Adiciona o produto filtrado à lista
        page.update()  # Atualiza a página para refletir as mudanças

    def filtrar_produtos_combinados(nome_produto, preco_maximo):
        try:
            preco_maximo = float(preco_maximo) if preco_maximo else float('inf')  # Define um valor infinito se o preço não for fornecido
            lista_produtos = get_produtos()
            produtos_filtrados = [
                p for p in lista_produtos
                if nome_produto.lower() in p['nome'].lower() and p['preco'] <= preco_maximo
            ]
            return produtos_filtrados
        except ValueError:
            print("Erro: O preço deve ser um número válido.")
            return []

    def atualizar_lista_produtos_filtrados_combinados(nome_produto, preco_maximo):
        produto_list.controls.clear()  # Limpa a lista de produtos exibida
        produtos_filtrados = filtrar_produtos_combinados(nome_produto, preco_maximo)  # Filtra os produtos
        for produto in produtos_filtrados:
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
            produto_list.controls.append(produto_component)  # Adiciona o produto filtrado à lista
        page.update()  # Atualiza a página para refletir as mudanças

        
    # Campo de busca para filtrar produtos por preço
    campo_busca_preco = ft.TextField(
        label="Filtrar por Preço Máximo",
        bgcolor="white",
        color="black",
        width=400,
        keyboard_type=ft.KeyboardType.NUMBER,
        on_change=lambda e: atualizar_lista_produtos_filtrados_combinados(campo_busca_produto.value, e.control.value),
    )

    campo_busca_preco_container = ft.Container(
        content=campo_busca_preco,
        alignment=ft.alignment.center,
        padding=ft.padding.all(10),
    )
    
    campo_busca_produto = ft.TextField(
        label="Buscar Produto",
        bgcolor="white",
        color="black",
        width=400,
        on_change=lambda e: atualizar_lista_produtos_filtrados_combinados(e.control.value, campo_busca_preco.value),
    )

    campo_busca_produto_container = ft.Container(
        content=campo_busca_produto,
        alignment=ft.alignment.center,
        padding=ft.padding.all(10),
    )


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

    button_add_pedido = ft.ElevatedButton(
        text="Adicionar no pedido", 

        
        on_click=lambda e: create_pedido(quantidade.value, page.mesa_id, buscar_id_produto_por_nome(add_list_produto.value)),)
    
    add_list_produto = ft.Dropdown(

    width=200,
    options=[
        ft.DropdownOption(text=produto['nome']) for produto in get_produtos()
    ],
    
    on_change=lambda e: print(f"Produto selecionado: ID={add_list_produto.value}"),
    )

    quantidade = ft.TextField(hint_text="Digite Quantidade:")

    # Lista de pedidos
    pedidos_list = ft.Column(
        scroll=ft.ScrollMode.ALWAYS,
        expand=True,
        spacing=10,
    )

    add_list_pagamento = ft.Dropdown(
        width=200,
        options=[
            ft.dropdown.Option("Pix"),
            ft.dropdown.Option("Cartão de Crédito"),
            ft.dropdown.Option("Cartão de Débito"),
            ft.dropdown.Option("Dinheiro"),
            ft.dropdown.Option("Vale Refeição"),
            ft.dropdown.Option("Berries"),
        ],
    )


    add_list_desconto = ft.Dropdown(
        width=200,  
        options=[
            ft.dropdown.Option("Flamengo"),
            ft.dropdown.Option("One Piece"),
            ft.dropdown.Option("Sousa"),
        ],
    )

    bs_pagamento = ft.BottomSheet(
        content=ft.Container(
            padding=50,
            content=ft.Column(
                tight=True,
                controls=[
                    ft.Text("Selecione o método de pagamento"),
                    add_list_pagamento,
                    ft.Text("Selecione o desconto"),
                    add_list_desconto,
                    ft.ElevatedButton(
                        "Fechar Pedido",
                        bgcolor="green", 
                        color="white", 
                        on_click=lambda e: fechar_pedido(add_list_pagamento.value, page.mesa_id_pagamento),
            )],
            ),
        ),
    )

    def fechar_pedido(metodo_pagamento, mesa_id):
        print(f"Pedido fechado para a mesa {mesa_id} com método de pagamento: {metodo_pagamento}")
        
        apagar_pedidos_mesa(mesa_id)  
        atualizar_lista_mesas()
        page.close(bs_pagamento)
        voltar()




    # Atualize o BottomSheet para exibir os pedidos
    bs_adicionar_pedido = ft.BottomSheet(
        content=ft.Container(
            padding=50,
            content=ft.Column(
                tight=True,
                controls=[
                    quantidade,
                    add_list_produto,
                    button_add_pedido,
                    
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
   
    
    atualizar_dropdown_produtos()
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

"""if __name__ == "__main__":
    # Teste simples para verificar a função get_pedidos_por_mesa
    mesa_id_teste = 1  # Substitua pelo ID de uma mesa existente no banco
    pedidos = get_pedidos_por_mesa(mesa_id_teste)
    print(f"Pedidos para a mesa {mesa_id_teste}: {pedidos}")"""
