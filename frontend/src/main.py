import flet as ft
from utils.mesas import get_mesas, create_mesa, delete_mesa, atualizar_status_mesa
from utils.produtos import get_produtos, create_produto, delete_produto, update_produto
from utils.pedidos import create_pedido, get_pedidos_por_mesa, apagar_pedidos_mesa, update_pedido, delete_pedido
from utils.relatorios import create_relatorio, get_relatorios_view
from utils.usuarios import get_usuarios, create_usuario, delete_usuario

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


    # -------------Funcoões de configuração da página------------------   
    
    # Função para criar o cabeçalho
    def criar_header(numero_mesa):
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
                                f"Bem vindo, {page.atual_usuario}",
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color="black",
                            ),
                            ft.Text(
                                f"Mesas Disponíveis: {numero_mesa}",
                                size=12,
                                color="black",
                            ),
                            ft.Row(
                                controls=[
                                    ft.ElevatedButton(
                                        text="Login",
                                        icon=ft.Icons.LOGIN,
                                        bgcolor="green",
                                        color="white",
                                        on_click=lambda e: criar_tela_login(),
                                    ),
                                    ft.ElevatedButton(
                                        text="Sair",
                                        icon=ft.Icons.LOGOUT,
                                        bgcolor="red",
                                        color="white",
                                        on_click=lambda e: criar_visitante(),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.END,  
                                spacing=10,  
                            )

                            

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

    # Função para volta a página inicial
    def voltar():
        if page.views:
            while len(page.views) > 1:
              page.views.pop()
            page.update()

    # Função para mudar de abas
    def change_page(event):
        # Limpa o conteúdo atual da aba
        conteudo.content.controls.clear()

        # Verifica qual aba foi selecionada
        if event.control.selected_index == 0: 
            atualizar_lista_mesas(layout_principal)
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
                ft.Column(
                    controls=[
                        campo_busca_produto_container,
                        campo_busca_preco_container,
                        button_add_produto_container,
                       
                    ],
                    
                    alignment=ft.MainAxisAlignment.START,
                    )
                
            )
            conteudo.content.controls.append(
                ft.Container(
                    content=produto_list,
                    expand=True,
                ),
            )
        
        elif event.control.selected_index == 2:
            page.update()
            print (page.permissao)
            if permissao_relatorio(page.permissao):
                
                atualizar_lista_relatorios()
                conteudo.content.controls.append(
                    ft.Column(
                        controls=[
                            button_add_usuario,
                        ],
                        
                        alignment=ft.MainAxisAlignment.END,
                        )
                    
                )

                conteudo.content.controls.append(
                    ft.Container(
                        content=relatorio_list,
                        expand=True,
                    ),
                )
            else:
                conteudo.content.controls.append(
                    
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(
                                "Acesso Restrito!",
                                size=21,
                                color="black",
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,  # Centraliza o texto na linha
                    ),
                    padding=10,
                    margin=3,
                    border_radius=10,
                    bgcolor="white",
                    border=ft.border.all(1, "black"),
                )
            )

        
        page.update()

    # -----------------Funções de gerenciamento de mesas------------------

    # Função para criar uma nova mesa
    def adicionar_mesa():

        numero_nova_mesa = len(get_mesas()) + 1

        if create_mesa(numero_nova_mesa):
            atualizar_lista_mesas(layout_principal)
            print(f"Mesa {numero_nova_mesa} criada com sucesso!")
        else:
            print("Erro ao criar a mesa.")

    # Função para atualizar a lista de mesas
    def atualizar_lista_mesas(layout_principal):

        numero_mesa = len(get_mesas())

        header = criar_header(numero_mesa)
        layout_principal.controls[0] = header

        mesa_list.controls.clear()
        lista_mesas = sorted(get_mesas(), key=lambda mesa: mesa['numero'])

        for mesa in lista_mesas:
            
             
            mesa_component = ft.Container(
                content=ft.ListTile(

                    title=ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(
                                f"Mesa {mesa['numero']:02d}",
                                size=21,
                                weight=ft.FontWeight.BOLD,
                                color="black",
                            ),
                            ft.Container(expand=True),
                            
                            ft.Container(
                                content=ft.Text(
                                    f"{'Disponível' if mesa['status'] else 'Indisponível'}",
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    color="white",
                                ),
                                alignment=ft.alignment.center,
                                bgcolor="green" if mesa['status'] else "red",
                                padding=ft.padding.symmetric(vertical=5),
                                border_radius=30,
                                width=130,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    padding=ft.padding.only(bottom=60),
                ),

                    
                subtitle= ft.Row(
                    controls=[

                        ft.Row(
                                controls=[
                                        
                                    ft.ElevatedButton(
                                        text="Adicionar",
                                        icon=ft.Icons.ADD,
                                        bgcolor="green",
                                        color="white",
                                        on_click=lambda e, mesa_id=mesa["id"], numero_mesa=mesa["numero"]: adicionar_pedido(
                                            mesa_id, numero_mesa
                                            )
                                            if permissao_usuario(page.permissao) else criar_tela_login(),
                        
                                        ),
                                    ft.ElevatedButton(
                                        text="Ver Pedidos",
                                        icon=ft.Icons.LIST,
                                        bgcolor="blue",
                                        color="white",
                                        on_click=lambda e, mesa_id=mesa["id"], numero_mesa=mesa["numero"]: exibir_pedidos(
                                                mesa_id, numero_mesa
                                            )
                                            if permissao_usuario(page.permissao) else criar_tela_login(),
                                        ),
                                    ft.ElevatedButton(
                                        text="Excluir",
                                        icon=ft.Icons.DELETE,
                                        bgcolor="red",
                                        color="white",
                                        on_click=lambda e, mesa_id=mesa["id"]: excluir_mesa(mesa_id) if permissao_usuario(page.permissao) else criar_tela_login(),
                                        ),
                                    ],
                                
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  
                                )
                            

                            ],
                            alignment=ft.MainAxisAlignment.END,
                            
                    ),
                
                ),
                padding=10,
                margin=3,
                border_radius=10,
                bgcolor="white",
                border=ft.border.all(1, "black"),
            )
            mesa_list.controls.append(mesa_component)
        page.update()

    # Função para excluir uma mesa
    def excluir_mesa(mesa_id):
        if delete_mesa(mesa_id):
            atualizar_lista_mesas(layout_principal)

    # ---------------Funções de gerenciamento de pedidos------------------

    # Função para adicionar um pedido
    def adicionar_pedido(mesa_id, numero_mesa):
        page.open(bs_adicionar_pedido)
        page.mesa_id = mesa_id

        page.update()
        button_add_pedido.on_click = lambda e: finalizar_adicao_pedido(mesa_id, numero_mesa)
        atualizar_lista_mesas(layout_principal)

    # Função para p
    def pagamento_pedido(mesa_id, valor_total, numeracao_mesa):
        page.mesa_id_pagamento = mesa_id
        page.valor_total_pago = valor_total
        page.numero_mesa_atual = numeracao_mesa

        print(f"Estou na {mesa_id}")

        page.close(bs_pagamento)
        page.update()

        page.open(bs_pagamento)
        page.update()

    # Função para exibir pedidos de uma mesa
    def exibir_pedidos(mesa_id, numeracao_mesa):

        print(f"numeracao mesa: {numeracao_mesa}")
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
                                    size=12, color="black"),
                                    trailing=ft.PopupMenuButton(
                                    key=pedido['pedido_id'],
                                    icon=ft.Icons.MORE_VERT,
                                    items=[
                                       ft.PopupMenuItem(
                                            text="Editar",
                                            icon=ft.Icons.EDIT,
                                            on_click=lambda e, pedido_id=pedido['pedido_id']: abrir_editar_pedido(pedido_id, mesa_id, numeracao_mesa),
                                        ),
                                        ft.PopupMenuItem(
                                            text="Excluir",
                                            icon=ft.Icons.DELETE, 
                                            on_click=lambda e, pedido_id=pedido['pedido_id']: excluir_pedido(pedido_id, mesa_id, numeracao_mesa),
                                        )
                                    ]
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
                 ft.Container(
                    content=ft.Text(f"Mesa Disponível, nenhum pedido encontrado.", size=16, color="black"),
                    bgcolor="white",
                    padding=10,
                    margin=5,
                    border_radius=10,
                    border=ft.border.all(1, "black"),
                )
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
            on_click=lambda e: pagamento_pedido(mesa_id, valor_total, numeracao_mesa),
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
                                f"Mesa {numeracao_mesa}",
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
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
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
        

        page.update()

    # Função para abrir o BottomSheet de edição de pedido
    def abrir_editar_pedido(pedido_id, id_mesa, mesa_numero):
        
        page.pedido_id = pedido_id
        page.mesa_id = id_mesa

        page.numero_mesa = mesa_numero
       
        pedido = next((p for p in get_pedidos_por_mesa(id_mesa) if p["pedido_id"] == pedido_id), None)

        print("Estou aqui meu REI")
        print("Rise")

        if pedido:
            
            page.nova_quantidade = str(pedido["quantidade"])
            page.novo_produto = pedido["produto_nome"]
           
            page.open(bs_editar_pedido)
            page.update()

    # Função para excluir um pedido
    def excluir_pedido(pedido_id, mesa_id, numero_mesa):
        if delete_pedido(pedido_id):
            exibir_pedidos(mesa_id, numero_mesa)

            atualizar_status_mesa(mesa_id, numero_mesa)
            atualizar_lista_mesas(layout_principal)

    # Função para fechar o pedido
    def fechar_pedido(mesa_id, numero_mesa, tipo_desconto, metodo_pagamento, valor_total):

        quantidade_pedidos = len(get_pedidos_por_mesa(mesa_id))
        
        desconto_valor = 0.0

        if tipo_desconto != None:
            desconto_valor = valor_total
            valor_total = 0.0
        
        else :
            tipo_desconto = "Nenhum"
        
        
        create_relatorio(
            numero_mesa,
            tipo_desconto,
            metodo_pagamento,
            desconto_valor,
            valor_total,
            quantidade_pedidos,
        )

        apagar_pedidos_mesa(mesa_id)  
        atualizar_lista_mesas(layout_principal)
        voltar()

  # Função para finalizar a adição de um pedido
    def finalizar_adicao_pedido(mesa_id, numero_mesa):
       
        
        quantidade_valor = quantidade.value
        produto_nome = add_list_produto.value

        # Verifica se os valores são válidos
        if not quantidade_valor or not produto_nome:
            print("[finalizar_adicao_pedido] Quantidade ou produto não selecionado.")
            return

        # Busca o ID do produto pelo nome
        produto_id = buscar_id_produto_por_nome(produto_nome)
        if produto_id is None:
            print(f"[finalizar_adicao_pedido] Produto '{produto_nome}' não encontrado.")
            return

        
        create_pedido(quantidade_valor, mesa_id, produto_id)

        
        #page.close(bs_adicionar_pedido)

        atualizar_status_mesa(mesa_id, numero_mesa)
        
        atualizar_lista_mesas(layout_principal)

        page.update()

    # Função para atualizar o pedido
    def atualizar_pedido(pedido_id, nova_quantidade_value, id_mesa, novo_produto):
        try:
            
            nova_quantidade = int(nova_quantidade_value.value) 

            
            produto_id = buscar_id_produto_por_nome(novo_produto)

            if produto_id is not None:
              
                if update_pedido(pedido_id, nova_quantidade, id_mesa, produto_id):

                    print(f"Pedido {pedido_id} atualizado com sucesso!")
                    exibir_pedidos(page.mesa_id, page.numero_mesa)
                    page.close(bs_editar_pedido)
                    atualizar_lista_mesas(layout_principal)
                    
                    page.update()
                else:
                    print("Erro ao atualizar o pedido.")
            else:
                print(f"Produto '{novo_produto}' não encontrado.")
        except ValueError:
            print("Erro: A quantidade deve ser um número válido.")


#-----------------Funções de gerenciamento de produtos------------------

    # Função para adicionar um novo produto
    def adicionar_produto(nome, preco):
        try:
            preco = float(preco)  
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

    # Função para atualizar a lista de produtos por ID
    def atualizar_produtos_por_id():
        global produtos_por_id
        produtos_por_id = {produto['id']: produto for produto in get_produtos()}

    # Função para atualizar a lista de produtos
    def atualizar_produtos(nome, preco):
        try:
            preco = float(preco)  
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
  
    # Função para atualizar o dropdown de produtos
    def atualizar_dropdown_produtos():
        lista_produtos = get_produtos()  
        add_list_produto.options = [
            ft.DropdownOption(lista_produtos[i]['nome']) for i in range(len(lista_produtos))
        ]
        page.update()  

    # Função para atualizar a lista de produtos
    def atualizar_lista_produtos():
        produto_list.controls.clear()
        
        lista_produtos = sorted(get_produtos(), key=lambda produto: produto['nome'])
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
                                on_click=lambda e, produto_id=produto['id']: abrir_editar_produto(produto_id) if permissao_usuario(page.permissao) else criar_tela_login()
                            ),
                            ft.PopupMenuItem(
                                text="Excluir",
                                icon=ft.Icons.DELETE,
                                on_click=lambda e, produto_id=produto['id']: excluir_produto(produto_id) if permissao_usuario(page.permissao) else criar_tela_login()
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

    # Função para filtrar produtos combinados
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

    # Função para atualizar a lista de produtos filtrados
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


    #-----------------Funções de gerenciamento de relatórios------------------

    # Função para atualizar a lista de relatórios
    def atualizar_lista_relatorios():
        relatorio_list.controls.clear()

        lista_relatorios = sorted(get_relatorios_view(), key=lambda relatorio: relatorio['numero_mesa'])
        print(lista_relatorios[0])
        print(lista_relatorios[0]["data_hora"])
      
        for relatorio in lista_relatorios:
            
            relatorio_component = ft.Container(
            content=ft.ListTile(
                title=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text(
                                    f"Mesa {relatorio['numero_mesa']}",
                                    size=21,
                                    weight=ft.FontWeight.BOLD,
                                    color="black",
                                ),
                                ft.Text(
                                    f"R$ {relatorio['valor_total']}",
                                    size=18,
                                    color="black",
                                    weight=ft.FontWeight.BOLD,
                                ),

                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                    ],
                    spacing=20,  
                ),
                subtitle=ft.Column(
                    controls=[
                        ft.Text(f"Desconto: {relatorio['desconto']}", size=12, color="black"),
                        ft.Text(f"Tipo de Desconto: {relatorio['tipo_desconto']}", size=12, color="black"),
                        ft.Text(f"Forma de Pagamento: {relatorio['tipo_pagamento']}", size=12, color="black"),
                        ft.Text(f"Quantidade de Pedidos: {relatorio['quantidade_pedidos']}", size=12, color="black"),
                        ft.Text(f"Data: {relatorio["data_hora"].strftime("%d/%m/%Y")}", size=12, color="black"),
                        ft.Text(f"Horario: {relatorio['data_hora'].strftime("%H:%M:%S")}", size=12, color="black"),
                    ],
                    spacing=5, 
                ),
            ),
            padding=10,
            margin=5,
            border_radius=10,
            bgcolor="white",
            border=ft.border.all(1, "black"),
        )
            relatorio_list.controls.append(relatorio_component)

        page.update()



    #-------------------------Funções de Usuario------------------------------

    # Função para ver se o usuário existe
    def verificar_usuario(nome, senha):
        usuarios = get_usuarios()
        
        usuario = next((u for u in usuarios if u['nome'] == nome and u['senha'] == senha), None)
        
        if usuario:
            return True
        else:
            return False

    # Função para adicionar um novo usuário
    def adicionar_usuario(nome, senha, cargo):
        try:
            print(get_usuarios())
            if not verificar_usuario(nome, senha):
                if create_usuario(nome, senha, cargo):
                    print(f"Usuario {nome} criado com sucesso!")
                    nomeUsuario_field.value = ""
                    senhaUsuario_field.value = ""
                    add_list_usuario.value = ""
                    page.update()
                else:
                    print("Erro ao criar o usuario.")

        except ValueError:
            print("Erro: O preço deve ser um número válido.")

    # Função para logar o usuário
    def login_usuario(nome, senha):
        if verificar_usuario(nome, senha):
            print(f"Login bem-sucedido para o usuário: {nome}")
            
            lista_usuarios = get_usuarios()
            usuario = next((u for u in lista_usuarios if u['nome'] == nome), None)
            page.usuario_atual = usuario
            page.atual_usuario = usuario['nome']
            page.permissao = usuario['cargo']
             
            atualizar_lista_mesas(layout_principal)
            voltar()

            page.update()
        else:
            print("Nome de usuário ou senha incorretos.")
    
    # Função para criar um visitante
    def criar_visitante():
        page.atual_usuario = "Visitante"
        page.permissao = "Visitante"
        atualizar_lista_mesas(layout_principal)
        page.update()

    #-------------------------------Login---------------------------------------

    # Função para criar a tela de login
    def criar_tela_login():
        """
        Função para criar a tela de login.
        """
        # Plano de fundo da tela de login
        fundo_login = ft.Container(
            width=400,
            height=800,
            content=ft.Image(
                src="image/background.png",
                fit=ft.ImageFit.COVER,
            ),
        )

        # Campos de entrada para nome de usuário e senha
        campo_nome_usuario = ft.TextField(
            label="Nome de Usuário",
            width=300,
            bgcolor="white",
            color="black",
            border_radius=15,
        )

        campo_senha_usuario = ft.TextField(
            label="Senha",
            width=300,
            bgcolor="white",
            color="black",
            border_radius=15,
            password=True,  # Oculta o texto digitado
        )

        # Botão para realizar o login
        botao_login = ft.ElevatedButton(
            text="Login",
            bgcolor="green",
            color="white",
            on_click=lambda e: login_usuario(campo_nome_usuario.value, campo_senha_usuario.value),
        )
        botao_voltar = ft.ElevatedButton(
            text="Voltar",
            bgcolor="red",
            color="white",
            on_click=lambda e: voltar(),
        )

        # Cabeçalho da tela de login
        cabecalho_login = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Image(
                        src="image/Icon.png",
                        fit=ft.ImageFit.COVER,
                        width=100,
                        height=100,
                        border_radius=5,
                    ),
                    ft.Text(
                        "Bem-vindo ao Restaurante Bom Sabor",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color="black",
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=10,
            border_radius=20,
            bgcolor="white",
            width=400,
            border=ft.border.all(1, "black"),
            margin=5,
        )

        # Layout principal da tela de login
        camada_login = ft.Container(
            alignment=ft.alignment.top_center,
            content=ft.Column(
                controls=[
                    cabecalho_login,
                    campo_nome_usuario,
                    campo_senha_usuario,
                    botao_login,
                    botao_voltar,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
            padding=20,
        )
        
        
        # Adiciona o plano de fundo e a camada ao Stack

        

        page.views.append(
            ft.View(
                "/login",
                controls=[
                    ft.Stack(
                        controls=[
                            fundo_login,  # Plano de fundo
                            camada_login,  # Camada de conteúdo
                        ],
                        expand=True,
                    )
                ],
            )
        )

        page.update()
    
    # Funções para verificar a permissão do usuário
    def permissao_usuario(cargo):
        if cargo == "Gerente":
            return True
        elif cargo == "Funcionario":
            return True
        else:
            return False

    def permissao_relatorio(cargo):
        if cargo == "Gerente":
            return True
        else:
            return False



    fundo = ft.Container(
        width=400,
        height=800,
        content=ft.Image(
            src="image/background.png",  
            fit=ft.ImageFit.COVER,  
        )
    )
    
    
    nome_field = ft.TextField(
        label="Nome do Produto",
        autofill_hints=ft.AutofillHint.NAME,
    )

    preco_field = ft.TextField(
        label="Preço",
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    nomeUsuario_field = ft.TextField(
        label="Nome do Usuario",
        autofill_hints=ft.AutofillHint.NAME,
    )

    senhaUsuario_field = ft.TextField(
        label="Senha do Usuario",
        keyboard_type=ft.KeyboardType.TEXT,
        password=True,
    )

    quantidade_field = ft.TextField(
        label="Quantidade",
        keyboard_type=ft.KeyboardType.NUMBER,
        on_change=lambda e: setattr(page, "quantidade", e.control.value),)

    quantidade = ft.TextField(hint_text="Digite Quantidade:")

    page.atual_usuario = "Visitante"
    page.permissao = "Visitante"

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

    add_list_usuario = ft.Dropdown(
        width=200,
        options=[
            ft.dropdown.Option("Gerente"),
            ft.dropdown.Option("Funcionario"),
        ],
    )

    add_list_produto = ft.Dropdown(
        width=200,
        options=[
            ft.DropdownOption(text=produto['nome']) for produto in get_produtos()
        
        ],
        on_change=lambda e: print(f"Produto selecionado: ID={add_list_produto.value}"),
            )

    #Botão para adicionar produto
    button_add_produto = ft.ElevatedButton(
        text="Adicionar Produto",
        bgcolor="green",
        color="white",
        on_click=lambda e: page.open(bs) if permissao_usuario(page.permissao) else criar_tela_login(),
    )

    #Botão para adicionar produto
    button_add_usuario = ft.ElevatedButton(
        text="Adicionar Usuario",
        bgcolor="green",
        color="white",
        on_click=lambda e: page.open(bs_usuario) if permissao_usuario(page.permissao) else criar_tela_login(),
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
        on_click=lambda e: adicionar_mesa() if permissao_usuario(page.permissao) else criar_tela_login(),
    )

    # Container para o botão de adicionar mesa
    button_add_container = ft.Row(
        controls=[button_add],
        alignment=ft.MainAxisAlignment.END,
    ) 


    button_add_pedido = ft.ElevatedButton(
        text="Adicionar no pedido", 
        on_click=lambda e: create_pedido(quantidade.value, page.mesa_id, buscar_id_produto_por_nome(add_list_produto.value)),)
    
    
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

    bs_usuario = ft.BottomSheet(
        content=ft.Container(
            padding=50,
            content=ft.Column(
                tight=True,
                controls=[
                    nomeUsuario_field,
                    senhaUsuario_field,
                    add_list_usuario,
                    ft.ElevatedButton("Cadastrar Usuario",
                    on_click=lambda e: adicionar_usuario(nomeUsuario_field.value, senhaUsuario_field.value, add_list_usuario.value)),
                ],
            ),
        ),
    )
    
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

    

    bs_editar_pedido = ft.BottomSheet(
        content=ft.Container(
            padding=50,
            content=ft.Column(

                tight=True,
                controls=[
                quantidade_field,
                ft.Dropdown(
                    label="Produto",
                    width=200,
                    options=[
                        ft.DropdownOption(produto["nome"]) for produto in get_produtos()
                    ],
                    on_change=lambda e: setattr(page, "novo_produto", e.control.value),
                ),
                ft.ElevatedButton(
                    "Atualizar Pedido",
                    bgcolor="green",
                    color="white",
                    on_click=lambda e: atualizar_pedido(
                        page.pedido_id, quantidade_field, page.mesa_id, page.novo_produto
                    ),
                ),
            ],
            ),
        ),
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
                        on_click=lambda e: fechar_pedido(page.mesa_id_pagamento, page.numero_mesa_atual, add_list_desconto.value, add_list_pagamento.value, page.valor_total_pago),
            )],
            ),
        ),
    )




    
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

    

    relatorio_list = ft.Column(
            scroll=ft.ScrollMode.ALWAYS,  
            expand=True,
            spacing=10,
    )


    # Lista de pedidos
    pedidos_list = ft.Column(
        scroll=ft.ScrollMode.ALWAYS,
        expand=True,
        spacing=10,
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

    # Campo de busca para filtrar produtos por preço
    campo_busca_preco = ft.TextField(
        label="Filtrar por Preço Máximo",
        bgcolor="white",
        color="black",
        border_radius=15,
        width=400,
        keyboard_type=ft.KeyboardType.NUMBER,
        on_change=lambda e: atualizar_lista_produtos_filtrados_combinados(campo_busca_produto.value, e.control.value),
    )

    campo_busca_preco_container = ft.Container(
        content=campo_busca_preco,
        alignment=ft.alignment.center,
        padding=ft.padding.symmetric(horizontal=10)
    )
    
    campo_busca_produto = ft.TextField(
        label="Buscar Produto",
        bgcolor="white",
        color="black",
        border_radius=15,
        width=400,
        on_change=lambda e: atualizar_lista_produtos_filtrados_combinados(e.control.value, campo_busca_preco.value),
    )

    campo_busca_produto_container = ft.Container(
        content=campo_busca_produto,
        alignment=ft.alignment.center,
        padding=ft.padding.symmetric(horizontal=10)
    )


    
    numero_mesa = len(get_mesas())

    # Adicionar a barra de navegação fixa no rodapé
    layout_principal = ft.Column(
        controls=[
            criar_header(numero_mesa),
            ft.Container(
                content=conteudo,
                expand=True,
            ),
            nav_bar,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        expand=True,
    )

    atualizar_dropdown_produtos()
    atualizar_lista_produtos()
    atualizar_lista_mesas(layout_principal)
    
    
    
    app = App()
    content.controls.append(app)
    page.overlay.append(bs)
    page.overlay.append(bs_editar)
    page.overlay.append(bs_editar_pedido)
    page.overlay.append(bs_pagamento)
    page.overlay.append(bs_adicionar_pedido)
    
    
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
