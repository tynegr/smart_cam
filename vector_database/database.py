from uuid import uuid4
import qdrant_client
from pydantic import BaseModel
from qdrant_client.http import models
import os
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")



class Item(BaseModel):
    embedding: list
    payload: dict


class Database:
    def __init__(self) -> None:
        self.collection_name = "test1"
        self.client = qdrant_client.QdrantClient(url="http://172.20.0.2:6333"
            # host=QDRANT_HOST,
            # port=QDRANT_PORT,
        )
        if not self.client.collection_exists(collection_name=self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=512,
                    distance=models.Distance.COSINE,
                ),
            )

    def insert(self, items: list[Item]):
        vectors = [item.embedding for item in items]
        payloads = [item.payload for item in items]
        point_ids = [uuid4().hex for _ in range(len(items))]
        self.client.upsert(
            collection_name=self.collection_name,
            points=models.Batch(
                ids=point_ids,
                payloads=payloads,
                vectors=vectors,
            ),
            wait=True,
        )

    def search(self, item: Item):
        embedding = item.embedding
        payload = item.payload
        filters = models.Filter(
            must=[
                models.FieldCondition(
                    key="category",
                    match=models.MatchValue(
                        value=payload["category"],
                    ),
                ),

            ],
        )

        response = self.client.search(
            collection_name=self.collection_name,
            query_vector=embedding,
            query_filter=filters,
            # limit=N_CHUNKS,
        )
        print(response[0].payload["price"])
        return response[0].payload["price"]


    def delete_points(self, data: dict):
        document_id = data["document_id"]
        return self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="document_id",
                            match=models.MatchValue(value=document_id),
                        ),
                    ],
                ),
            ),
        )