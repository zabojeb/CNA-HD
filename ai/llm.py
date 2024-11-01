from openai import OpenAI
from os import getenv

CHAT_MODEL = "nousresearch/hermes-3-llama-3.1-405b:free"
OPENROUTER_API_KEY = "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"

def process_message_debug(session):
    messages = session["messages"]

    uploaded_data = session["uploaded_data_file_path"]
    description = session["description"]
    address = session["address"]

    last_message = messages[-1]

    return f"Описание: {description}\nАдрес: {address}\nВаше сообщение: {last_message}"

def process_message(session):
    messages = []
    for message in session["messages"]:
        messages.append({"role": "user",
                         "content": [
                             {
                                 "type": "text",
                                 "text": message
                             }
                             ]
                         })

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
          
          Основная информация об отеле, описание которого тебе нужно сгенерировать:
          1. Геолокация/адрес: {address}
          2. Описание: {description}
          """
        }
      ]
    }
    
    # gets API Key from environment variable OPENROUTER_API_KEY to prevent api key leak
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )

    completion = client.chat.completions.create(
    model=CHAT_MODEL,
    messages=[system_message] + messages
    )

    return completion.choices[0].message.content