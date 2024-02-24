import functions as fn
import flet as ft
from flet.matplotlib_chart import MatplotlibChart


def main(page: ft.Page):
    page.title = "Calculadora de errores de laboratorio"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.appbar = ft.AppBar(
        title=ft.Text(
            "Calculadora de errores de laboratorio", weight=ft.FontWeight.BOLD, color=ft.colors.BLACK87
        ),
        bgcolor=ft.colors.BLUE,
        center_title=True,
        actions=[
            ft.IconButton(ft.icons.MENU, tooltip="Menu",
                          icon_color=ft.colors.BLACK87)
        ],
        color=ft.colors.WHITE,
    )

    def btn_click(e):
        if not txt_name.value:
            txt_name.error_text = "Please enter the formula"
            page.update()
        else:
            name = txt_name.value
            # Here changed the variables, I'm trying to make an interface to select them
            b = fn.calculate_error(name, ['g', 'N'])
            fig = fn.render_formula(b)
            page.add(MatplotlibChart(fig, expand=True))
            page.set_clipboard(b)
            page.update()

    txt_name = ft.TextField(label="Your formula")

    page.add(txt_name)

    C = ft.ElevatedButton("Calculate", on_click=btn_click)

    dlg = ft.AlertDialog(
        title=ft.Text(""" Usage \t To use this calculator enter your latex formula, click evaluate to add the value of the constants 
                      \t and then click calculate """), on_dismiss=lambda e: print("Dialog dismissed!")
    )

    def close_dlg(e):
        dlg.open = False
        page.update()

    def open_dlg(e):
        page.dialog = dlg
        dlg.open = True
        page.update()
    I = ft.ElevatedButton("Instructions", on_click=open_dlg)

    def btn_click2(e):
        if not txt_name.value:
            txt_name.error_text = "Please enter the formula"
            page.update()
        else:
            name = txt_name.value
            vars = fn.detect_var(name)
            row = []
            for i in vars:
                fig = fn.render_formula(i)
                row.append(MatplotlibChart(fig, expand=True, scale=0.5))
            r2 = ft.Row([ft.Container(expand=1, content=j) for j in row])
            page.add(r2)
            page.update()
    E = ft.ElevatedButton("Evaluate", on_click=btn_click2)
    r = ft.Row([
        ft.Container(expand=1, content=C),
        ft.Container(expand=1, content=E),
        ft.Container(expand=1, content=I)
    ])
    page.add(r)


ft.app(target=main)
