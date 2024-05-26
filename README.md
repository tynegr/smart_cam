# Название команды - Демон и Андроид(и Андроид)

# Состав команды: 
- Егор Тищенко(@egor_jpeg)
- Михаил Щербаков(@Mikhail_oil_car)

 # Проект № 15 - умная камера 

 # Инструкция по запуску:
- скачиваем данные по ссылке: https://drive.google.com/file/d/1s8dy0yGBCr3vdM-xBfmHHzqrdxQJHP7x/view?usp=sharing 
- распоковываем их и кладем в root директорию проекта
- make network 
- make run_qdrant
- make build_model_client
- make build_vector_client
- make build_smart_cam
- make run_model_client
- make run_vector_client
- docker exec -it vector_client_container python /app/add_data.py
- make run_smart_cam 

