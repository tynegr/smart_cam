from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel
import io
from config import MODEL_PATH, MODEL_HOST, MODEL_PORT, MODEL_NAME
from vector_database.database import Database, Item
import pandas as pd
import numpy as np
import os
import time
import requests

model = CLIPModel.from_pretrained(MODEL_PATH)
processor = CLIPProcessor.from_pretrained(MODEL_NAME)
database = Database()


df = pd.read_csv('/Users/oleg/Downloads/final_df.csv')
# print(df)
# Уникальные значения столбца rightmost_nonnull
unique_labels = df['category'].dropna().unique().tolist()


# Папка с изображениями
image_folder = 'aaa_advml_project'

# embeddings = {}

url = 'http://127.0.0.1:8007/add'

for _, row in df.iterrows():
    # start_time = time.time()
    image_id = row['external_image_id']
    category = [row['category']]
    image_path = os.path.join(image_folder, f"{image_id}.jpg")
    print(image_path)
    if os.path.exists(image_path):
        # Загрузка изображения
        with open(image_path, 'rb') as img_file:
            image = Image.open(io.BytesIO(img_file.read()))
            # Подготовка входных данных для модели
            inputs = processor(text=[row['category']], images=image,
                               return_tensors="pt", padding=True)
            # Прогон данных через модель
            outputs = model(**inputs)
            # Получение эмбеддингов
            image_embeds = outputs.image_embeds
            # Сохранение эмбеддингов
            # embeddings[image_id] = image_embeds.tolist()[0]

            data = {'embeddings': [image_embeds.tolist()[0]], 'price': row['price'],
                    'category': row['category']}

            res = requests.post(url, json=data)
            # print(len(embeddings[image_id]))


    # end_time = time.time()
    # print(end_time - start_time)

# Вывод эмбеддингов для каждой картинки
# for image_id, embedding in embeddings.items():
#     print(f"Image ID: {image_id}, Embedding: {embedding}")


