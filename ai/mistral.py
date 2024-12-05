from mistralai import Mistral
import time
import base64
import copy
import os

CHAT_MODEL = "pixtral-large-latest"
DESCRIPTION_MODEL = "mistral-large-latest"

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

FULL_PROMPT = open("./ai/prompt.txt", "r", encoding="utf-8").read()


def encode_image(image_path):
    """Encode the image to base64."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except FileNotFoundError:
        print(f"Error: The file {image_path} was not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def process_message(session):
    messages = copy.deepcopy(session["messages"])

    for i, message in enumerate(messages):
        if message["role"] == "user":
            for j, content in enumerate(message["content"]):
                if content["type"] == "image_url":
                    messages[i]["content"][j]["image_url"] = (
                        "data:image/jpeg;base64,"
                        + encode_image(messages[i]["content"][j]["image_url"])
                    )

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
          
          Придерживайся этого плана:
          {FULL_PROMPT}
          
          НИ В КОЕМ СЛУЧАЕ НЕ ПИШИ ОПИСАНИЕ ОТЕЛЯ В СООБЩЕНИЯ!!! ПИШИ ЕГО С ПОМОЩЬЮ ТВОЕЙ ФУНКЦИИ!!!
          
          Стартовое описание отеля, предоставленное пользователем:
          {description}
          """,
            }
        ],
    }

    client = Mistral(
        api_key=MISTRAL_API_KEY,
    )

    completion = client.chat.complete(
        model=CHAT_MODEL,
        messages=[system_message] + messages,
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "generate_description",
                    "description": "Сгенерировать описание для отеля на основе новой полученной информации.",
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
          
          При генерации придерживайся этого плана:
          {FULL_PROMPT}
          
          ИСПОЛЬЗУЙ ВСЕ ВОЗМОЖНОСТИ РАЗМЕТКИ MARKDOWN
          
          Стартовое описание отеля, предоставленное пользователем и его пожелания:
          """,
                }
            ],
        },
        {"role": "user", "content": [{"type": "text", "text": info}]},
    ]

    client = Mistral(
        api_key=MISTRAL_API_KEY,
    )

    completion = client.chat.complete(
        model=DESCRIPTION_MODEL,
        messages=messages,
    )

    print("Description generated!")

    return completion.choices[0].message.content
