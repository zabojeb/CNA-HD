# CNA-HD
### Contextual Neural Assistant for Hotel Description

---
## Навигация по файлам
- [main.py](https://github.com/zabojeb/CNA-HD/blob/main/main.py) - это главный файл, который координирует работу всех процессов, описывает эндпоинты и поведение сайта
- [ai/llm.py](https://github.com/zabojeb/CNA-HD/blob/main/ai/llm.py) и [ai/main.py](https://github.com/zabojeb/CNA-HD/blob/main/ai/main.py) - это файлы, в которых происходит взаимодействие с нейросетями, там есть функции для получения описания и для обработки информации от пользователя
- в папке [notebooks](https://github.com/zabojeb/CNA-HD/tree/main/notebooks) можно увидеть наши наработки по дополнительным функциям. Наиболее информативны файлы [map_result.ipynb](https://github.com/zabojeb/CNA-HD/blob/main/notebooks/map_result.ipynb) - это файл с наиболее рабочими наработками по картам и анализу геолокации (менее удачные варианты показаны в файлах [testcords.ipynb](https://github.com/zabojeb/CNA-HD/blob/main/notebooks/testcords.ipynb) и [testmap2.ipynb](https://github.com/zabojeb/CNA-HD/blob/main/notebooks/testmap2.ipynb)); [parser.ipynb](https://github.com/zabojeb/CNA-HD/blob/main/notebooks/parser.ipynb) -это файл с имеющимися парсерами; [sentiment_analysis.ipynb](https://github.com/zabojeb/CNA-HD/blob/main/notebooks/sentiment_analysis.ipynb) - это файл, в котором представлен полный анализ отзывов со всеми результатами и этапами работы, а также некоторые парсеры


## Обзор
CNA-HD - это инструмент, использующий искусственный интеллект для автоматизации процесса создания всесторонних и персонализированных описаний отелей. Система использует передовые модели обработки естественного языка, методы компьютерного зрения и анализ контекстуальных данных, чтобы генерировать информативные и привлекательные описания отелей, которые учитывают потребности потенциальных клиентов.

## Ключевые преимущества
1. **Контекстуальный анализ**: Система анализирует различные контекстуальные факторы, такие как местоположение, близлежащие достопримечательности, транспорт, мероприятия и отзывы пользователей, чтобы создавать описания, подчеркивающие уникальные преимущества отеля.
2. **Персонализация**: CNA-HD адаптирует описания отелей к индивидуальным предпочтениям и потребностям каждого клиента, обеспечивая, что контент соответствует их конкретным интересам.
3. **Итеративный подход**: Система позволяет владельцам отелей предоставлять отзывы и дополнительную информацию, что позволяет ассистенту постоянно совершенствовать и улучшать описания отелей со временем.
4. **Масштабируемость**: CNA-HD разработан для работы с большим количеством отелей, автоматически интегрируя обновленную информацию и адаптируясь к уникальным характеристикам каждого объекта.
5. **Плавная интеграция**: Система может быть легко интегрирована в существующие платформы бронирования отелей, обеспечивая бесшовный пользовательский опыт для клиентов.

## Используемые технологии
- **Обработка естественного языка**: ruBERT, RuBERTa и другие передовые языковые модели для анализа тональности, аспектно-ориентированного анализа тональности и генерации текста.
- **Компьютерное зрение**: DETR, YOLO и CLIP для обнаружения объектов, сопоставления изображений и текста, а также визуального анализа.
- **Геопространственные данные**: Overpass API, OSMnx, Яндекс.Карты API и OpenWeatherMap API для сбора информации, основанной на местоположении.
- **Бэкенд**: Flask, Python3
- **Фронтенд**: HTML5, CSS3, JavaScript

## Использование
CNA-HD может использоваться владельцами отелей, платформами бронирования и другими участниками индустрии гостеприимства для генерации высококачественных, персонализированных описаний отелей, которые привлекают и вовлекают потенциальных клиентов.

## Дорожная карта
- **MVP**: Реализация основного функционала системы, включая контекстный анализ, персонализацию и итеративное улучшение.
- **Доработка решения (мы тут)**: Включение дополнительных функций
- **Готовый продукт**: Расширение системы дополнительными возможностями, такими как интеграция динамических данных (например, мероприятия, погода), поддержка нескольких языков и расширенная визуализация данных.
- **Пост продакшн**: Исследование интеграции CNA-HD с другими связанными с гостеприимством сервисами и изучение потенциала для коммерциализации.

## Технические подробности
- **Архитектура**: CNA-HD использует микросервисную архитектуру, где каждый модуль (анализ геолокации, анализ фото, анализ отзывов, генерация описаний) реализован как отдельный сервис. Это повышает гибкость, масштабируемость и возможность модульной замены компонентов.
- **Модели ML**: Для анализа отзывов используются русскоязычные модели BERT и RuBERTa, предварительно обученные на задачах анализа тональности и извлечения аспектов. Для обнаружения объектов на фотографиях применяется модель DETR, а для сопоставления изображений и текста - CLIP.
- **Хранение данных**: Мы собираемся хранить данные в обьектном хранилище S3 от Yandex Cloud.
- **Интеграция**: CNA-HD интегрируется с внешними API (Яндекс.Карты, OpenWeatherMap, Eventbrite) для получения дополнительной контекстной информации. Готовые описания отелей могут экспортироваться в различные форматы (Markdown, HTML) для публикации на сторонних платформах.

## Прототип
В прототипе мы использовали библиотеку openai и провайдера OpenRouter. Библиотека openai очень удобна тем, что мы можем легко поменять провайдера. **В том числе реализовать своё API и использовать модели с Hugging Face.**

Демонстрация доступна по [ссылке](http://38.180.168.36/)
