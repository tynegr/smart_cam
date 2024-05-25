from fastapi import FastAPI, UploadFile
import uvicorn
import io
import imageio.v3 as iio
import cv2
from transformers import CLIPProcessor, CLIPModel
from config import MODEL_PATH, MODEL_HOST, MODEL_PORT, MODEL_NAME
import torch
from PIL import Image
import numpy as np


app = FastAPI()

model = CLIPModel.from_pretrained(MODEL_PATH)
processor = CLIPProcessor.from_pretrained(MODEL_NAME)

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
    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=1)
    _, predicted = torch.max(probs, 1)
    predicted_label = labels[predicted.item()]
    return {"embeddings": image_embeds.tolist(),"label": predicted_label}


@app.post("/embed_video")
async def embed_video(file: UploadFile):
    # Read the uploaded file
    contents = await file.read()
    video_stream = iio.imiter(contents, plugin="pyav")

    frames = []
    for frame in video_stream:
        frame = np.array(frame)
        frames.append(frame)

    resized_frames = [cv2.resize(frame, (512, 512)) for frame in frames]

    video_embeddings = []
    for frame in resized_frames:
        image = Image.fromarray(frame)
        labels = ["футболка Gucci", "пляж"]
        inputs = processor(text=labels, images=image, return_tensors="pt",
                           padding=True)
        outputs = model(**inputs)
        image_embeds = outputs.image_embeds
        video_embeddings.append(image_embeds)

    video_embedding = torch.mean(torch.stack(video_embeddings), dim=0)

    return {"embeddings": video_embedding.tolist()}


uvicorn.run(app, host=MODEL_HOST, port=MODEL_PORT)
