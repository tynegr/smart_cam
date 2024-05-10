from fastapi import FastAPI, UploadFile
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel
import uvicorn
import io
from config import MODEL_PATH, MODEL_HOST, MODEL_PORT, MODEL_NAME
from vector_database.database import Database, Item

app = FastAPI()

model = CLIPModel.from_pretrained(MODEL_PATH)
processor = CLIPProcessor.from_pretrained(MODEL_NAME)
database = Database()

@app.post("/predict")
async def predict(file: UploadFile):
    try:
        image = Image.open(io.BytesIO(await file.read()))
    except Exception as e:
        return {"error": str(e)}
    labels = ["футболка Gucci", "футболка Prada", "футболка Гуччи", "футболка Фенди"]
    inputs = processor(text=labels, images=image, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=1)
    _, predicted = torch.max(probs, 1)
    predicted_label = labels[predicted.item()]
    return {"predicted_label": predicted_label}


@app.post("/embed")
async def embed(file: UploadFile):
    image = Image.open(io.BytesIO(await file.read()))
    labels = ["футболка Gucci", "футболка Prada", "футболка Гуччи", "футболка Фенди"]
    inputs = processor(text=labels, images=image, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    image_embeds = outputs.image_embeds
    return {"embeddings": image_embeds.tolist()}


uvicorn.run(app, host=MODEL_HOST, port=MODEL_PORT)
