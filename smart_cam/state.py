import reflex as rx
import requests
import json

class State(rx.State):
    price: str = ''

    async def handle_upload(self, files: list[rx.UploadFile]):
        for file in files:
            upload_data = await file.read()
            self.price = ""
            yield
            try:
                response = requests.post("http://model_client:8006/embed", files={"file": upload_data})
            except Exception as e:
                response = ""

            if not response:
                try:
                    response = requests.post("http://model_client:8006/embed_video", files={"file": upload_data})
                except Exception as e:
                    pass

            if response:
                print(response.text)
                json_data = json.loads(response.text)
                embedding = json_data["embeddings"]
                category = json_data["category"]
                response = requests.post("http://vector_client:8007/search", json = {"embeddings":embedding,"category":category})
                self.price = response.text
            else:
                self.price = "Unsupported File format"





