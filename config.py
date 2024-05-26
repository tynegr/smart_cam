import os
MODEL_PATH = "/app/vector_database/clip-vit-base-patch16"
# MODEL_PATH = "/Users/egortishchenko/PycharmProjects/smart_cam/vector_database/clip-vit-base-patch16"
MODEL_URL = "http://model_client_container44:8006"
VECTOR_URL = "http://vector_client_container44:8007"
MODEL_HOST = "0.0.0.0"
MODEL_PORT = 8006
MODEL_NAME = "openai/clip-vit-base-patch16"
QDRANT_HOST = "0.0.0.0"
QDRANT_PORT = 8007
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
