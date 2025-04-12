import flet as ft
from flet import View

def _view_():
    return View(
        "/conta",
        controls=[
            ft.Column(
                [
                    ft.Text("Página de Conta", size=20),
                    ft.TextField(label="Nome"),
                    ft.TextField(label="Email"),
                    ft.TextField(label="Senha", password=True),
                    ft.ElevatedButton("Voltar", on_click=lambda e: e.page.go("/")),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        ]
    )