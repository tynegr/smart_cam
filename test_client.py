import requests
from config import MODEL_URL

image_path = "http://images.cocodataset.org/val2017/000000039769.jpg"

response = requests.post("http://127.0.0.1:8006/embed ", json={"url": image_path})

if response.status_code == 200:
    result = response.json()
    print(result)
else:
    print(f"Error: {response.status_code} - {response.text}")
