from fastapi import FastAPI
from vector_database.database import Database, Item
import uvicorn
from config import QDRANT_HOST, QDRANT_PORT


database = Database()
app = FastAPI()

@app.post("/add", status_code=200)
async def add(data: dict):
        embedding = data["embeddings"]
        items = [
            Item(
                embedding=embedding[0],
                payload={
                    "document_id": "sheryaev",

                },
            )
        ]
        database.insert(items)


@app.post("/search")
async def search(data: dict) -> list:
    embedding = data["embeddings"]
    print(embedding)
    item = Item(
        embedding=embedding[0],
        payload={

            "document_id": "sheryaev",
        },
    )
    return database.search(item)


uvicorn.run(app, host=QDRANT_HOST, port=QDRANT_PORT)
