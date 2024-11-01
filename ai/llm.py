def generate_hotel_description(
    hotel_data: dict, extra_prompt: str, conversation_history: list
) -> str:
    import torch
    from llama_cpp import Llama
    from pathlib import Path

    # Путь к модели
    mistral_models_path = Path.home().joinpath("mistral_models", "8B-Instruct")
    model_path = (
        "./mistral-7b-instruct-v0.2.Q4_K_M.gguf"  # Проверьте формат и имя файла модели
    )

    # Инициализация модели с использованием llama_cpp
    model = Llama(model_path=str(model_path), n_ctx=2048, n_gpu_layers=20)
    # Формируем промпт для генерации описания с учетом всей истории сообщений
    prompt = f"""
    На основе следующих сообщений сгенерируй благоприятное описание отеля '{hotel_data['hotel_name']}' для привлечения гостей.
    - Местоположение: {hotel_data['location']}
    - Категория: {hotel_data['category']}
    - Удобства: {hotel_data['amenities']}
    - Особенности: {hotel_data['features']}
    {extra_prompt}

    История сообщений:
    """

    # Добавляем в промт все сообщения отельера
    for i, message in enumerate(conversation_history):
        prompt += f"\nСообщение {i + 1}: {message}"

    # Генерация текста с помощью llama_cpp
    result = model(prompt, max_tokens=2500, temperature=0.7)
    return result["choices"][0]["text"]


# Функция для обработки сообщений от отельера
def handle_user_message(hotel_data: dict, extra_prompt: str):
    global conversation_history

    # Бесконечный цикл для интерактивного ввода сообщений
    while True:
        # Ввод сообщения от пользователя (отельера)
        user_message = input(
            "Введите сообщение для улучшения описания отеля (или 'exit' для выхода): "
        )

        # Если пользователь вводит 'exit', цикл прерывается
        if user_message.lower() == "exit":
            break

        # Добавляем сообщение в историю
        conversation_history.append(user_message)

        # Генерация описания отеля с учетом всей истории сообщений
        description = generate_hotel_description(
            hotel_data, extra_prompt, conversation_history
        )


def process_message(session):
    messages = session["messages"]

    uploaded_data = session["uploaded_data_file_path"]
    description = session["description"]
    address = session["address"]

    last_message = messages[-1]
    data = {
        "hotel_name": "Солнечный Берег",
        "location": "Сочи, Россия",
        "category": "4-звездочный",
        "amenities": "Бассейн, спа-центр, ресторан, бесплатный Wi-Fi",
        "features": "Расположение рядом с пляжем, панорамный вид на море, семейные номера",
    }
    # description = generate_hotel_description(
    #     data,
    #     last_message,
    #     messages,
    # )

    return f"Описание: {description}\nАдрес: {address}\nВаше сообщение: {last_message}"
