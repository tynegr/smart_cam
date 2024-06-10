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

            if file.filename.endswith('.mp4'):
                response = requests.post("http://172.20.0.3:8006/embed_video",
                                         files={"file": upload_data})
            else:

                try:
                    response = requests.post("http://172.20.0.3:8006/embed", files={"file": upload_data})
                except Exception as e:
                    response = ""

            if response:
                print(response.text)
                json_data = json.loads(response.text)
                embedding = json_data["embeddings"]
                category = json_data["label"]
                response = requests.post(f"http://172.20.0.4:8007/search", json={"embeddings": embedding, "label": category})
                self.price = response.text
            else:
                self.price = "Unsupported File format"

