import pandas as pd
import requests
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import io
from config import MODEL_PATH, MODEL_NAME
from vector_database.database import Database
import os
import numpy as np

df = pd.read_csv('avito_df_final.csv')
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
train_size = int(0.8 * len(df))
train_df = df[:train_size]
test_df = df[train_size:]

# url = 'http://172.20.0.4:8007/search'

url = 'http://0.0.0.0:8007/search'

image_folder = 'aaa_advml_project'

model = CLIPModel.from_pretrained(MODEL_PATH)
processor = CLIPProcessor.from_pretrained(MODEL_NAME)
database = Database()

real_prices = []
predicted_prices = []

total_rows = len(test_df)
current_row = 0

for _, row in test_df.iterrows():
    if current_row == 100:
        break
    image_id = row['external_image_id']
    category = [row['category']]
    image_path = os.path.join(image_folder, f"{image_id}.jpg")
    print(image_path)

    with open(image_path, 'rb') as img_file:
        image = Image.open(io.BytesIO(img_file.read()))
        inputs = processor(text=[row['category']], images=image,
                           return_tensors="pt", padding=True)
        outputs = model(**inputs)
        image_embeds = outputs.image_embeds

        data = {'embeddings': [image_embeds.tolist()[0]],
                'label': row['category']}

        res = requests.post(url, json=data)

        print(res.status_code)

        real_price = row['price']

        try:

            pred_price = float(res.text)
            print(real_price - pred_price)

        except Exception as e:
            continue

        real_prices.append(real_price)
        predicted_prices.append(pred_price)
        current_row += 1


real_prices = np.array(real_prices)
predicted_prices = np.array(predicted_prices)
mae = np.mean(abs(real_prices - predicted_prices))
print(f'Mean Absolute Error: {mae}')
