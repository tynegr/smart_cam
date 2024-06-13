from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import io
from config import MODEL_PATH, MODEL_NAME
from vector_database.database import Database
import pandas as pd
import os
import requests

model = CLIPModel.from_pretrained(MODEL_PATH)
processor = CLIPProcessor.from_pretrained(MODEL_NAME)
database = Database()


df = pd.read_csv('avito_df_final.csv')

unique_labels = df['category'].dropna().unique().tolist()


image_folder = 'aaa_advml_project'


url = 'http://172.20.0.4:8007/add'

total_rows = len(df)
current_row = 0

for _, row in df.iterrows():
    image_id = row['external_image_id']
    category = [row['category']]
    image_path = os.path.join(image_folder, f"{image_id}.jpg")
    print(image_path)

    if os.path.exists(image_path):
        with open(image_path, 'rb') as img_file:
            image = Image.open(io.BytesIO(img_file.read()))
            inputs = processor(text=[row['category']], images=image,
                               return_tensors="pt", padding=True)
            outputs = model(**inputs)
            image_embeds = outputs.image_embeds

            data = {'embeddings': [image_embeds.tolist()[0]], 'price': row['price'],
                    'category': row['category']}

            res = requests.post(url, json=data)

    current_row += 1
    print(f"Progress: {current_row}/{total_rows} rows processed")





