from flask.json import jsonify
from app import db
from flask import redirect, request, render_template
from flask_classy import FlaskView, route
from ..auth.decorators import check_auth
from ..auth.utils import get_auth_instance
from ..auth.models import User
from app import mail
from flask_mail import Message
from app.exceptions import DefaultExceptions

class Account(FlaskView):

    #получение данных пользователя
    @check_auth
    def get(self):
        id, claims = get_auth_instance().get_current_user_data_from_token()   
        return jsonify(claims), 200        

    #получение/заполнение формы с данными пользователя
    @check_auth
    @route("/settings/", methods=["GET", "POST"])
    def set_account(self):        
        uid, claims = get_auth_instance().get_current_user_data_from_token()
        if request.method == 'POST':
            #TODO: написать загрузку аватарки            
            
            if request.json.get("delete"):
                return redirect('/delete/'), 303
                       
            user = User.query.filter_by(id = uid).first()
            user.nickname = request.json.get("nickname")
            user.first_name = request.json.get("first_name")
            user.last_name = request.json.get("last_name")
            user.email = request.json.get("email")
            user.telegram_nickname = request.json.get("telegram_nickname")
            db.session.commit()
            
            return redirect('/settings/'), 303

        return jsonify(nickname=claims['nickname'], first_name=claims['first_name'],
        last_name=claims['last_name'], email=claims['email'],
        telegram_nickname=claims['telegram_nickname']), 200

    #удаление аккаунта пользователя с сообщением о причине
    @check_auth    
    @route('/delete/', methods=["GET", "POST"])
    def delete_account(self):
        uid, claims = get_auth_instance().get_current_user_data_from_token() 
        if request.method == 'POST':

            user_message = request.json.get("user_message")
                                   
            msg = Message("Сообщение об удалении аккаунта пользователем %s" % claims['nickname'],
                recipients=['justbeginnoreply@gmail.com'])
            msg.body = user_message
            mail.send(msg)

            user = User.query.filter_by(id = uid).first()
            db.session.delete(user)
            db.session.commit()

            return redirect("/home/"), 303

        return jsonify(nickname = claims["nickname"]), 200




