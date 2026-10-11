import flet as ft
from frontend.src.views.root.root_view import RootView


async def main(page: ft.Page):
    root = RootView(page)


if __name__ == "__main__":
    ft.run(main, assets_dir="frontend/src/assets")
