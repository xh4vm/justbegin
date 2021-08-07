from flask import render_template
from wtforms.validators import ValidationError, DataRequired, Length, Email
from wtforms.form import Form
from wtforms import StringField, SubmitField

class SettingsForm(Form):
    nickname = StringField(validators=[DataRequired(), Length(min=3, max=64)])
    first_name = StringField()
    last_name = StringField()
    email = StringField(validators=[DataRequired(), Email(), Length(max=128)])
    telegram_nickname = StringField()

    submit = SubmitField(label=('Сохранить'))
    delete = SubmitField(label=('Удалить аккаунт'))

class DeleteFeedback(Form):
    message = StringField(validators=[DataRequired()])
    submit = SubmitField(label=('Удалить аккаунт'))