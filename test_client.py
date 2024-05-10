import requests
from config import MODEL_URL

image_path = "/path"

response = requests.get(MODEL_URL, params={"image_path": image_path})

if response.status_code == 200:
    result = response.json()
    print(f"Predicted label: {result['predicted_label']}")
else:
    print(f"Error: {response.status_code} - {response.text}")
