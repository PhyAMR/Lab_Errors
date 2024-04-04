import functions as fn
import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import functools


def main(page: ft.Page):
    page.title = "Calculadora de errores de laboratorio"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

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

    txt_name = ft.TextField(label="Your formula")

    page.add(txt_name)

    dlg = ft.AlertDialog(
        title=ft.Text(""" Usage \n To use this calculator enter your latex formula, click evaluate to add the value of the constants 
                       and then click calculate """), on_dismiss=lambda e: print("Dialog dismissed!")
    )

    def close_dlg(e):
        dlg.open = False
        page.update()

    def open_dlg(e):
        page.dialog = dlg
        dlg.open = True
        page.update()

    I = ft.ElevatedButton("Instructions", on_click=open_dlg)
    const = []

    def btn_click2(e):
        if not txt_name.value:
            txt_name.error_text = "Please enter the formula"
            page.update()
        else:
            name = txt_name.value
            form = fn.convert_latex_to_sympy(name)
            vars = fn.detect_var(name)

            # Lista para almacenar los campos de texto
            text_fields = []

            # Crear los campos de texto para introducir los valores
            for var in vars:
                text_field = ft.TextField(label=f"Enter value for {var}")
                text_fields.append(text_field)
                page.add(ft.Container(expand=1, content=text_field))

            # Actualizar la página para mostrar los campos de texto
            page.update()

            # Esperar a que el usuario introduzca los valores
            input_values = []
            for field in text_fields:
                while True:
                    if field.value is not None and field.value.strip() != "":
                        try:
                            input_values.append(float(field.value))
                            break
                        except ValueError:
                            # El usuario introdujo un valor no numérico, pedir de nuevo
                            field.error_text = "Please enter a valid number"
                            page.update()
                    else:
                        # El campo está vacío, pedir al usuario que lo complete
                        field.error_text = "Please enter a number"
                        page.update()

            # Crear el diccionario de sustitución
            sub = dict(zip(vars, input_values))

            # Evaluar la fórmula con los valores ingresados
            result = form.evalf(subs=sub)
            print("Result:", result)

            page.update()

    def calc(e, form, vars, text_fields):
        # Obtener los valores ingresados por el usuario
        input_values = [float(field.value) for field in text_fields]

        # Crear el diccionario de sustitución
        sub = dict(zip(vars, input_values))

        # Evaluar la fórmula con los valores ingresados
        result = form.evalf(subs=sub)
        print("Result:", result)

    def btn_click(e):
        if not txt_name.value:
            txt_name.error_text = "Please enter the formula"
            page.update()
        else:
            name = txt_name.value
            form = fn.calculate_error(name, const)
            fig = fn.render_formula(form)
            page.add(MatplotlibChart(fig, scale=1))
            page.set_clipboard(form)
            page.update()

    C = ft.ElevatedButton("Calculate", on_click=btn_click)
    E = ft.ElevatedButton("Evaluate", on_click=btn_click2)
    r = ft.Row([
        ft.Container(expand=1, content=E),
        ft.Container(expand=1, content=C),
        ft.Container(expand=1, content=I)
    ])
    page.add(r)


ft.app(target=main)
