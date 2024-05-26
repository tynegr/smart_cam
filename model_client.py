from fastapi import FastAPI, UploadFile
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel
import uvicorn
import io
from config import MODEL_PATH, MODEL_HOST, MODEL_PORT, MODEL_NAME
from vector_database.database import Database, Item
import pandas as pd

app = FastAPI()

model = CLIPModel.from_pretrained(MODEL_PATH)
processor = CLIPProcessor.from_pretrained(MODEL_NAME)
database = Database()
df = pd.read_csv('/Users/oleg/Downloads/final_df.csv')
# print(df)
# Уникальные значения столбца rightmost_nonnull
unique_labels = df['category'].dropna().unique().tolist()

@app.post("/predict")
async def predict(file: UploadFile):
    try:
        image = Image.open(io.BytesIO(await file.read()))
    except Exception as e:
        return {"error": str(e)}
    labels = unique_labels
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
    labels = unique_labels
    inputs = processor(text=labels, images=image, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    image_embeds = outputs.image_embeds
    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=1)
    _, predicted = torch.max(probs, 1)
    predicted_label = labels[predicted.item()]
    return {"embeddings": image_embeds.tolist(),"label": predicted_label}

uvicorn.run(app, host=MODEL_HOST, port=MODEL_PORT)
