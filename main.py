from flask import *
import os
from werkzeug.utils import secure_filename

from data.startform import StartForm

DEBUG = True

app = Flask(__name__)
app.config["SECRET_KEY"] = "OurSecretKeyisI2D"
UPLOAD_FOLDER = os.path.join("staticFiles", "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def index():
    return redirect("/start")


# переброс


@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "messages" not in session:
        session["messages"] = []
    if "uploaded_data_file_path" not in session:
        session["uploaded_data_file_path"] = None
    session.modified = True
    message = "Сообщение"
    # print(session["uploaded_data_file_path"])
    if request.method == "POST":
        # вызов какойто внешней функции с message
        message = request.form["message"]
        session["messages"].append(message)
        # тут надо азкинуть в историю и ответ нейронки
        session["messages"].append(message + " <-- ответ нейронки")

    return render_template(
        "chat.html",
        photo=session["uploaded_data_file_path"],
        messages=session["messages"],
    )


@app.route("/start", methods=["GET", "POST"])
def form():
    form = StartForm()
    if request.method == "POST":
        # print(form.photo.data.filename, secure_filename(form.photo.data.filename))
        if form.photo.data.filename:
            filename = form.photo.data.filename
            form.photo.data.save("uploads/" + filename)
            session["uploaded_data_file_path"] = os.path.join("./uploads/" + filename)
        else:
            session["uploaded_data_file_path"] = None
        session["description"] = form.description.data
        session["address"] = form.address.data
        session["url"] = url_for("chat")
        session["messages"] = []
        session.modified = True
        # + запуск gpt
        return redirect("/chat")
    return render_template("start.html", form=form)


@app.route("/sendmessage", methods=["POST"])
def sendmessage():
    return render_template("chat.html")


@app.errorhandler(404)
def page_not_found(e):
    return redirect("/start")


@app.route("/deletesession")
def deletesession():
    session.clear()
    return redirect("/start")


if __name__ == "__main__":
    app.run(debug=DEBUG)
