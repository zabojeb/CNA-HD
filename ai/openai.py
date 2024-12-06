from openai import OpenAI
import time
import os
from dotenv import load_dotenv

load_dotenv()
CHAT_MODEL = "openai/gpt-4o-mini"
DESCRIPTION_MODEL = "openai/gpt-4o-mini"

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def process_message(session):
    messages = session["messages"]

    uploaded_data = session["uploaded_data_file_path"]
    description = session["description"]
    address = session["address"]

    system_message = {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": f"""
          Ты - опытный специалист в сфере жилья и отелей.
          Твоя задача - составить хорошее привлекательное завлекающее описание отеля. Для этого тебе будет нужно общаться с пользователем-отельером и узнавать у него информацию об отеле.
          Задавай пользователю наводящие вопросы и старайся узнать как можно больше информации про отель.
          Если пользователь задаёт вопрос не по теме, то вежливо переведи обратно на тему генерации описания отеля.

          Основные категории информации:
          1. Геолокация: адрес, местоположение отеля, заведения и интересные места рядом с отелем
          2. Услуги: услуги, которые может предоставить отель - WiFi, кондиционер, завтраки, бассейн, спортзал и тд
          3. Особенности
          4. Фотографии отеля
          5. Другое
          
          Стартовое описание отеля, предоставленное пользователем:
          {description}
          """,
            }
        ],
    }

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )

    completion = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[system_message] + messages,
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "generate_description",
                    "description": "Сгенерировать описание для отеля на основе новой полученной информации. Вызывай эту функцию ТОЛЬКО когда пользователь добавил новые данные или когда попросил изменить описание.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "info": {
                                "type": "string",
                                "description": "Информация об отеле. Название, описание, услуги, любая информация, пожелания и тд. Включи сюда также пожелания пользователя об описании.",
                            },
                        },
                        "required": ["info"],
                    },
                },
            }
        ],
    )

    time.sleep(1)

    print("Message sent!")

    return completion


def generate_description(info):
    messages = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": f"""
          Ты - опытный специалист в сфере жилья и отелей.
          Твоя задача - составить хорошее привлекательное завлекающее описание отеля.
          Тебе будет предоставлено описание и вся нужная информация об отеле пользователя.
          
          Основные категории информации:
          1. Геолокация: адрес, местоположение отеля, заведения и интересные места рядом с отелем
          2. Услуги: услуги, которые может предоставить отель - WiFi, кондиционер, завтраки, бассейн, спортзал и тд
          3. Особенности
          4. Фотографии отеля
          5. Другое
          
          Стартовое описание отеля, предоставленное пользователем и его пожелания:
          """,
                }
            ],
        },
        {"role": "user", "content": [{"type": "text", "text": info}]},
    ]

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )

    completion = client.chat.completions.create(
        model=DESCRIPTION_MODEL,
        messages=messages,
    )

    print("Description generated!")

    return completion.choices[0].message.content
