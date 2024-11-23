#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from flask import *
from flask import session
import os
from werkzeug.utils import secure_filename

from data.startform import StartForm

from map import make_href_for_cords,find_cords

# Импорт ML функций для инференса
from ai.llm import process_message, generate_description


DEBUG = True

app = Flask(__name__)
app.config["SECRET_KEY"] = "OurSecretKeyisI2D"
UPLOAD_FOLDER = os.path.join("staticFiles", "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER




@app.route("/")
def index():
    return render_template("index.html")


# Редирект на чат
@app.route("/chat", methods=["GET", "POST"])
def chat():
    
    
    if "messages" not in session:
        session["messages"] = [
            {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": "Привет! Я - Оскар, ассистент от МТС, который поможет Вам составить идеальное описание для отеля. Начнём?",
                    }
                ],
            }
        ]
    if "description" not in session:
        session["description"] = "Нет описания"
    if "lat" not in session:
        session["lat"] = None
    if "lon" not in session:
        session["lon"] = None
    if "address" not in session:
        session["address"] = "Нет адреса"
    if "uploaded_data_file_path" not in session:
        session["uploaded_data_file_path"] = None
    if "ai_messages" not in session:
       session["ai_messages"] = [] + [session["description"]] # список сообщений от ассистента --------------------<<<<<< ДОБАВИТЬ НАДО СЮДА ТОЖЕ

    session.modified = True
    message = "Сообщение"

    if request.method == "POST":
        message = request.form["message"]
        session["messages"].append(
            {"role": "user", "content": [{"type": "text", "text": str(message)}]}
        )

        # process_message обрабатывает сообщение и возвращает ответ в виде str
        response = process_message(session)
        
        if response.choices[0].message.tool_calls:
            info = json.loads(response.choices[0].message.tool_calls[0].function.arguments)['info']

            generated_description = generate_description(info)
            session['ai_messages'].append(generated_description)

            assistant_message = "Описание сгенерировано!"
        else:
            assistant_message = response.choices[0].message.content

        session["messages"].append(
            {
                "role": "assistant",
                "content": [{"type": "text", "text": assistant_message}],
            })
    if session["lat"] and session["lon"]:
        session["map"] = make_href_for_cords([session["lat"], session["lon"]])
        print(session["map"], "Получили ссылку на карту")
        return render_template(
            "chat.html",
            photo=session["uploaded_data_file_path"],
            messages=session["messages"],
            map=session["map"],
            ai_messages=session["ai_messages"],
        )
    else:
               return render_template(
            "chat.html",
            photo=session["uploaded_data_file_path"],
            messages=session["messages"],
            map=None,
            ai_messages=session["ai_messages"],
        )
        #             {% if map %}
        # <p>{{ session["map"].to_html(full_html=False)|safe }}</p>
        # {% endif %}
    # else:
    #     session["map"] = None
    # return render_template(
    #     "chat.html",
    #     photo=session["uploaded_data_file_path"],
    #     messages=session["messages"],
    #     map=False,
    # )

@app.route("/start", methods=["GET", "POST"])
def form():
    form = StartForm()
    if request.method == "POST":
        if form.photo.data.filename:
            filename = form.photo.data.filename
            form.photo.data.save("./static/" + filename)
            session["uploaded_data_file_path"] = os.path.join(
                url_for("static", filename=filename)
            )
        else:
            session["uploaded_data_file_path"] = None

        session["description"] = form.description.data

        # a = findplace(form.address.data)
        # session["address"] = a["address"]
        session["address"] = form.address.data
        lat_and_lon_res = find_cords(form.address.data)
        print(lat_and_lon_res, "Получили координаты")
        if lat_and_lon_res:
            session["lat"] = lat_and_lon_res[0]
            session["lon"] = lat_and_lon_res[1]
            
        else:
            session["lat"] = None
            session["lon"] = None
        session["url"] = url_for("chat")
        session["ai_messages"] = [] 
        session["messages"] = [
            {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": "Привет! Я - Оскар, ассистент от МТС, который поможет Вам составить идеальное описание для отеля. Начнём?",
                    }
                ],
            }
        ]
        session["ai_messages"] = []
        session.modified = True

        # + запуск чата
        return redirect("/chat")

    return render_template("start.html", form=form)


@app.route("/sendmessage", methods=["POST"])
def sendmessage():
    return render_template("chat.html")


@app.errorhandler(404)
def page_not_found(e):
    return redirect("/")


@app.route("/deletesession")
def deletesession():
    session.clear()
    return redirect("/start")


if __name__ == "__main__":
    app.run(debug=DEBUG)
