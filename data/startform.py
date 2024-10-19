from flask_wtf import *
from wtforms import *
from wtforms.validators import *


class StartForm(FlaskForm):
    description = TextAreaField(
        "Введите описание",
        validators=[DataRequired()],
    )
    address = StringField(
        "Адрес",
        validators=[DataRequired()],
    )
    photo = FileField("Фото")
    submit = SubmitField('Войти в чат')