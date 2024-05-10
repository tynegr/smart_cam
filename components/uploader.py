import reflex as rx
from state import State

def upload_form():
    return rx.vstack(
        rx.heading("Загрузка файлов", align="center"),
        rx.divider(),
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
                "Загрузить",
                on_click=State.handle_upload(
                    rx.upload_files(
                        upload_id="upload3",
                    ),
                ),
            ))