.PHONY: all build_model_client build_vector_client build_smart_cam run_model_client run_vector_client run_smart_cam run_qdrant network clean

NETWORK_NAME := my_network
QDRANT_VOLUME := $(shell pwd)/qdrant_storage

all: network build_model_client build_vector_client build_smart_cam run_model_client run_vector_client run_smart_cam run_qdrant

network:
	docker network create $(NETWORK_NAME)

build_model_client:
	docker build -t model_client_image -f Dockerfile_model .

build_vector_client:
	docker build -t vector_client_image -f vector_database/Dockerfile_vector .

build_smart_cam:
	docker build -t smart_cam_image -f smart_cam/Dockerfile_main .

run_model_client:
	docker run -p 8006:8006 --rm --name model_client_container --network $(NETWORK_NAME) model_client_image

run_vector_client:
	docker run -p 8007:8007 --name vector_client_container --network $(NETWORK_NAME) vector_client_image

run_smart_cam:
	docker run -p 3000:3000 -p 8000:8000 --rm --name main_client_container --network $(NETWORK_NAME) smart_cam_image

run_qdrant:
	docker run -p 6333:6333 -p 6334:6334 --rm --name qdrant_container --network $(NETWORK_NAME) -v $(QDRANT_VOLUME):/qdrant/storage:z qdrant/qdrant

clean:
	docker network rm $(NETWORK_NAME)
