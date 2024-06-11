import requests
import time
import pandas as pd
import random
import os

df = pd.read_csv('test.csv')
unique_labels = df['category'].dropna().unique().tolist()


def measure_search_time(url, unique_labels, iterations=60):
    timings = []
    status_codes = set()

    for i in range(iterations):
        data = {"embeddings": [[x for x in range(i, i + 512)]],
                "label": random.choice(unique_labels)}
        response = requests.post(url, json=data)
        timings.append(response.elapsed.total_seconds())
        status_codes.add(response.status_code)
        time.sleep(1)

    average_time = sum(timings) / iterations
    return average_time, status_codes


def measure_embed_time(url, image_folder, df):
    timings = []
    status_codes = set()

    for _, row in df.iterrows():
        image_id = row['external_image_id']
        image_path = os.path.join(image_folder, f"{image_id}.jpg")

        if os.path.exists(image_path):
            with open(image_path, 'rb') as img_file:
                response = requests.post(url, files={"file": img_file})
                timings.append(response.elapsed.total_seconds())
                status_codes.add(response.status_code)
                time.sleep(1)

    average_time = sum(timings) / len(timings) if timings else 0
    return average_time, status_codes


search_url = "http://0.0.0.0:8007/search"
embed_url = "http://0.0.0.0:8006/embed"

average_search_time, status_codes_search = measure_search_time(search_url,
                                                               unique_labels)
print(f"Average search time: {average_search_time} seconds")
print(f"Status codes of /search: {status_codes_search}")

image_folder = 'aaa_advml_project'
average_embed_time, status_codes_embed = measure_embed_time(embed_url,
                                                            image_folder, df)
print(f"Average embed time: {average_embed_time} seconds")
print(f"Status codes of /embed: {status_codes_embed}")

average_service_time = average_search_time + average_embed_time
print(f"Average time of service: {average_service_time} seconds")
