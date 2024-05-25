import reflex as rx
from smart_cam.components.uploader import upload_form
from smart_cam.state import State


def index() -> rx.Component:
    return rx.center(rx.vstack(
        upload_form(),
        rx.text(State.price)
    ))


app = rx.App()
app.add_page(index)
