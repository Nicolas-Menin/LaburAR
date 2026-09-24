import flet as ft
from frontend.src.core.config import API_URL
# pylint: disable=E1121,E1123,E0401


def main(page: ft.Page):
    page.title = "LaburAR"
    page.window.width = 1200
    page.window.height = 800

    page.add(
        ft.Text(
            f"Backend: {API_URL}",
            size=32,
            weight=ft.FontWeight.BOLD,
        )
    )


if __name__ == "__main__":
    ft.run(main)