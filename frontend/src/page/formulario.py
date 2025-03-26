import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Lista para armazenar os produtos cadastrados
    produtos = []

    def handle_dismissal(e):
        page.add(ft.Text("Bottom sheet dismissed"))

    def cadastrar_produto(e):
        # Obtém os valores dos campos
        nome_produto = nome_field.value
        preco_produto = preco_field.value

        # Salva os dados na lista
        produtos.append({"nome": nome_produto, "preco": preco_produto})

        # Exibe uma mensagem de confirmação
        
        page.add(ft.Text(f"Produto '{nome_produto}' cadastrado com sucesso!"))

        # Fecha o BottomSheet
        page.close(bs)

    # Campos do formulário
    nome_field = ft.TextField(
        label="Nome do Produto",
        autofill_hints=ft.AutofillHint.NAME,
    )
    preco_field = ft.TextField(
        label="Preço",
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    bs = ft.BottomSheet(
        on_dismiss=handle_dismissal,
        content=ft.Container(
            padding=50,
            content=ft.Column(
                tight=True,
                controls=[
                    nome_field,
                    preco_field,
                    ft.ElevatedButton("Cadastrar Produto", on_click=cadastrar_produto),
                ],
            ),
        ),
    )
    page.add(ft.ElevatedButton("Abrir formulário de produto", on_click=lambda _: page.open(bs)))


ft.app(main)