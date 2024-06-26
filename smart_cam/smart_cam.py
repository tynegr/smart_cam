import reflex as rx
from smart_cam.state import State


def index() -> rx.Component:
    return rx.vstack(
        rx.heading("Загрузка файлов", align="center"),
        rx.upload(
            rx.text(
                "Перенесите файлы или нажмите, чтобы загрузить файл",
                align="center"
            ),
            id="upload3",
            border="1px dotted rgb(107,99,246)",
            padding="5em",
        ),
            rx.button(
                "Получить цену!",
                on_click=State.handle_upload(
                    rx.upload_files(
                        upload_id="upload3",
                    ),
                ),
            ),
        rx.cond(State.price,
        rx.text(f"Cправедливая цена: {State.price}")),
        align='center',
        margin_top="15em"
    )


app = rx.App()
app.add_page(index)
