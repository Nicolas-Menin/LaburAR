import flet as ft
from frontend.src.views.root.root_view import RootView


async def main(page: ft.Page):
    root = RootView(page)
    ruta_inicial = page.route or "/"

    if ruta_inicial == "/":
        ruta_inicial = "/login"
        await page.push_route(ruta_inicial)

    await root.route_change(
        type("RouteEvent", (), {"route": ruta_inicial})()
    )

if __name__ == "__main__":
    ft.run(main, assets_dir="frontend/src/assets")
