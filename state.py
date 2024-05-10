import reflex as rx
import requests
import json
from config import MODEL_URL

class State(rx.State):
    price: str = ''

    async def handle_upload(self, files: list[rx.UploadFile]):
        for file in files:
            upload_data = await file.read()
            response = requests.post("http://127.0.0.1:8006/embed", files={"file": upload_data})
            json_data = json.loads(response.text)
            embedding = json_data["embeddings"]
            response = requests.post("http://127.0.0.1:8007/search", json = {"embeddings":embedding})
            self.price = response.text




