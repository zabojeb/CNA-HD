#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import *
import os
from werkzeug.utils import secure_filename

from data.startform import StartForm
import osmnx as ox
import networkx as nx

from geopy.geocoders import Nominatim
import plotly
from map import plot_nearby_places

# Импорт ML функций для инференса
from ai.llm import process_message
import geopandas as gpd

DEBUG = True

app = Flask(__name__)
app.config["SECRET_KEY"] = "OurSecretKeyisI2D"
UPLOAD_FOLDER = os.path.join("staticFiles", "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def findplace(address):
    locator = Nominatim(user_agent="i2dd")
    location = locator.geocode(address)
    if location:
        return {"lat": location.latitude, "lon": location.longitude, "address": address}
    else:
        return {"address": address, "lat": None, "lon": None}


@app.route("/")
def index():
    return render_template("index.html")

# Редирект на чат
@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "messages" not in session:
        session["messages"] = [{"role": "assistant",
                         "content": [
                             {
                                 "type": "text",
                                 "text": "Привет! Я - Оскар, ассистент от МТС, который поможет Вам составить идеальное описание для отеля. Начнём?"
                             }
                             ]
                         }]
    if "description" not in session:
        session["description"] = "Нет описания"
    if "address" not in session:
        session["address"] = "Нет адреса"
    if "uploaded_data_file_path" not in session:
        session["uploaded_data_file_path"] = None

    session.modified = True
    message = "Сообщение"

    if request.method == "POST":
        message = request.form["message"]
        session["messages"].append({"role": "user",
                         "content": [
                             {
                                 "type": "text",
                                 "text": str(message)
                             }
                             ]
                         })

        # process_message обрабатывает сообщение и возвращает ответ в виде str
        assistant_message = process_message(session)

        session["messages"].append({"role": "assistant",
                        "content": [
                            {
                                "type": "text",
                                "text": assistant_message
                            }
                            ]
                        })
    if session["address"]:
        # session["map"] = plot_nearby_places(session["address"])
        # print(
        #     plotly.offline.plot(
        #         session["map"], include_plotlyjs=False, output_type="div"
        #     )
        # )
        # if session["map"]:
            # session["map"] = session["map"].to_html(full_html=False)
            return render_template(
                "chat.html",
                photo=session["uploaded_data_file_path"],
                messages=session["messages"],
                map=False,
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
        #session["address"] = a["address"]
        session["address"] = form.address.data
        # session["lat"] = a["lat"]
        # session["lon"] = a["lon"]
        session["lat"] = None
        session["lon"] = None
        session["url"] = url_for("chat")
        session["messages"] = []
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
