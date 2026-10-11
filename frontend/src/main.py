import flet as ft
from frontend.src.views.root.root_view import RootView


async def main(page: ft.Page):

    root = RootView(page)

    await page.push_route("/login")

    return root


if __name__ == "__main__":
    ft.run(main, assets_dir="frontend/src/assets")
