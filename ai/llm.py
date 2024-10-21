def process_message(session):
    messages = session["messages"]

    uploaded_data = session["uploaded_data_file_path"]
    description = session["description"]
    address = session["address"]

    last_message = messages[-1]

    return f"Описание: {description}\nАдрес: {address}\nВаше сообщение: {last_message}"
