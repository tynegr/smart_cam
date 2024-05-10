import reflex as rx
import requests
import json
from config import MODEL_URL

class State(rx.State):
    price: str = ''

    async def handle_upload(self, files: list[rx.UploadFile]):
        for file in files:
            upload_data = await file.read()
            response = requests.post(MODEL_URL, files={"file": upload_data})
            json_data = json.loads(response.text)
            self.price = json_data["predicted_label"]
