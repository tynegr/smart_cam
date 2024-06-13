# Название команды - Демон и Андроид(и Андроид)

# Состав команды: 
- Егор Тищенко(@egor_jpeg)
- Михаил Щербаков(@Mikhail_oil_car)

 # Проект № 15 - умная камера 
<img width="1194" alt="Снимок экрана 2024-06-13 в 09 56 25" src="https://github.com/tynegr/smart_cam/assets/122130536/0748946a-cf41-4ce9-a788-3c3e9b35a9bc">

 # Инструкция по запуску:
- скачиваем данные по ссылке: https://drive.google.com/file/d/1s8dy0yGBCr3vdM-xBfmHHzqrdxQJHP7x/view?usp=sharing 
- распоковываем их и кладем в root директорию проекта
- переходим  в папку "vector database" проекта и в консоли пишем: git clone https://huggingface.co/openai/clip-vit-base-patch16
- make network 
- make run_qdrant
- make build_model_client
- make build_vector_client
- make build_smart_cam
- make run_model_client
- make run_vector_client
- docker exec -it vector_client_container python /app/add_data.py
- make run_smart_cam 

