#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import shutil
from flask import Flask, request, redirect, url_for, render_template
from flask import *
from flask import session
import datetime
from itertools import accumulate
import os

from data.startform import StartForm

from map.map import make_href_for_cords, find_cords

INFERENCE_TYPE = "MISTRAL"  # ["MISTRAL", "OPENAI", "HUGGINGFACE"]
if INFERENCE_TYPE == "MISTRAL":
    from ai.mistral import process_message, generate_description
elif INFERENCE_TYPE == "OPENAI":
    from ai.openai import process_message, generate_description
elif INFERENCE_TYPE == "HUGGINGFACE":
    from ai.huggingface import process_message, generate_description

DEBUG = True

app = Flask(__name__)
app.config["SECRET_KEY"] = "OurSecretKeyisI2D"
UPLOAD_FOLDER = os.path.join("staticFiles", "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def pipeline_ai():
    response = process_message(session)

    if response.choices[0].message.tool_calls:
        info = json.loads(response.choices[0].message.tool_calls[0].function.arguments)[
            "info"
        ]

        generated_description = generate_description(info)
        session["ai_messages"].append(generated_description)

        assistant_message = "Описание сгенерировано!"
    else:
        assistant_message = response.choices[0].message.content

    session["messages"].append(
        {
            "role": "assistant",
            "content": [{"type": "text", "text": assistant_message}],
        }
    )


@app.route("/")
def index() -> str:
    """
    Root route for the app, renders the main page.

    Returns:
        str: The rendered HTML template.
    """
    return render_template("index.html")


# Редирект на чат
@app.route("/chat", methods=["GET", "POST"])
def chat():
    """
    Handles the chat functionality for the application.

    This function manages the session data for a chat between the user and the assistant.
    It initializes session variables if they do not exist, processes user messages, generates
    responses using AI, and updates the session with both user and assistant messages. The chat
    page is rendered with relevant data such as messages, a map link (if available), and any AI-generated
    descriptions.

    For GET requests, it ensures required session variables are set and renders the chat page.
    For POST requests, it processes the user's message, generates an AI response, updates the session,
    and renders the chat page with updated information.

    Returns:
        str: The rendered HTML template for the chat page.
    """
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
        session["uploaded_data_file_path"] = []
    if "ai_messages" not in session:
        session["ai_messages"] = [] + [
            session["description"]
        ]  # список сообщений от ассистента --------------------<<<<<< ДОБАВИТЬ НАДО СЮДА ТОЖЕ
    if "old_fp" not in session:
        session["old_fp"] = []

    message = "Сообщение"

    if request.method == "POST":
        message = request.form["message"]

        new_photos = list(
            set(session["uploaded_data_file_path"]) - set(session["old_fp"])
        )
        
        session["old_fp"] = session["uploaded_data_file_path"]
        
        if new_photos != []:
            content = [{"type": "text", "text": str(message)}]

            for photo in new_photos:
                content.append({"type": "image_url", "image_url": photo })

            session["messages"].append({"role": "user", "content": content})
        else:
            session["messages"].append(
                {"role": "user", "content": [{"type": "text", "text": str(message)}]}
            )

        pipeline_ai()


    session.modified = True

    # ОТОБРАЖЕНИЕ
    if session["lat"] and session["lon"]:
        session["map"] = make_href_for_cords([session["lat"], session["lon"]])
        print(session["map"], "Получили ссылку на карту")
        return render_template(
            "chat.html",
            photoes=session["uploaded_data_file_path"],
            messages=session["messages"],
            map=session["map"],
            ai_messages=session["ai_messages"],
        )
    else:
        return render_template(
            "chat.html",
            photoes=session["uploaded_data_file_path"],
            messages=session["messages"],
            map=None,
            ai_messages=session["ai_messages"],
        )


@app.route("/start", methods=["GET", "POST"])
def form():
    form = StartForm()
    if "uid" not in session:
        t = datetime.datetime.now().timestamp()
        session["uid"] = int(t)
    if request.method == "POST":
        if form.photo.data.filename:
            if "uploaded_data_file_path" not in session:
                session["uploaded_data_file_path"] = []
            newpath = f"./static/{session['uid']}/"
            filename = form.photo.data.filename
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            allpath = (
                newpath
                + str(len(session["uploaded_data_file_path"]) + 1)
                + "."
                + filename.split(".")[-1]
            )
            form.photo.data.save(allpath)

            session["uploaded_data_file_path"].append(os.path.join(allpath))
        else:
            session["uploaded_data_file_path"] = []

        session["description"] = form.description.data

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

        session["messages"] = []
        if session["description"]:
            session["messages"].append(
                {
                    "role": "user",
                    "content": [{"type": "text", "text": session["description"]}],
                }
            )
            pipeline_ai()

        else:
            session["messages"].append(
                {
                    "role": "assistant",
                    "content": [
                        {
                            "type": "text",
                            "text": "Привет! Я - Оскар, ассистент от МТС, который поможет Вам составить идеальное описание для отеля. Начнём?",
                        }
                    ],
                }
            )

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
    try:
        shutil.rmtree(f"./static/{session['uid']}")
    except Exception:
        pass
    session.clear()
    return redirect("/start")


@app.route("/attach_file", methods=["GET", "POST"])
def upload_file():
    print("attach_file")
    files = request.files.getlist("file")
    if request.method == "POST":
        if len(files) > 10:
            return "Вы можете загрузить максимум 10 файлов.", 400

        if "uploaded_data_file_path" not in session:
            session["uploaded_data_file_path"] = []

        for file in files:
            newpath = f"./static/{session['uid']}/"

            filename = file.filename

            if not os.path.exists(newpath):
                os.makedirs(newpath)

            allpath = (
                newpath
                + str(len(session["uploaded_data_file_path"]) + 1)
                + "."
                + filename.split(".")[-1]
            )
            file.save(allpath)

            session["uploaded_data_file_path"].append(os.path.join(allpath))

    print(session["uploaded_data_file_path"])

    session.modified = True

    return redirect("/chat")


if __name__ == "__main__":
    app.run(debug=DEBUG)
