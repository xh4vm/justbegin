from flask import render_template
from flask_wtf import FlaskForm
from flaskwtf import StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length, Email

class SettingsForm(FlaskForm):
    nickname = StringField(validators=[DataRequired(), Length(min=3, max=64)])
    first_name = StringField()
    last_name = StringField()
    email = StringField(validators=[DataRequired(), Email(), Length(max=128)])
    telegram_nickname = StringField()

    submit = SubmitField(label=('Сохранить'))
    delete = SubmitField(label=('Удалить аккаунт'))

class DeleteFeedback(FlaskForm):
    message = StringField(validators=[DataRequired()])
    submit = SubmitField(label=('Удалить аккаунт'))