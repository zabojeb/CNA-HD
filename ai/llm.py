from openai import OpenAI
import time

CHAT_MODEL = "openai/gpt-4o-mini"
OPENROUTER_API_KEY = "Secret"

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

    time.sleep(1)
    
    print(completion)
    
    return completion.choices[0].message.content