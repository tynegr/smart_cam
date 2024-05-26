from fastapi import FastAPI
from database import Database, Item
import uvicorn
from config import QDRANT_HOST, QDRANT_PORT


database = Database()
app = FastAPI()

@app.post("/add", status_code=200)
async def add(data: dict):
        embedding = data["embeddings"]
        price = data["price"]
        category = data["category"]
        items = [
            Item (
                embedding = embedding[0],
                payload = {
                    "category": category,
                    "price" : price,
                },
            )
        ]
        database.insert(items)


@app.post("/search")
async def search(data: dict) -> float:
    embedding = data["embeddings"]
    category = data["label"]
    print(embedding)
    item = Item(
        embedding=embedding[0],
        payload={

            "category": category,
        },
    )
    return database.search(item)


uvicorn.run(app, host=QDRANT_HOST, port=QDRANT_PORT)
