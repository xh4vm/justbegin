from flask.json import jsonify
from app import db
from flask import redirect, request, render_template
from flask_classy import FlaskView, route
from app.account import bp
from app.auth.decorators import check_auth
from app.auth.utils import get_auth_instance
from app.models import User
from app.account.forms import SettingsForm, DeleteFeedback
from app import mail
from flask_mail import Message

class Account(FlaskView):

    #получение данных пользователя
    @check_auth
    def get(self):
        id, claims = get_auth_instance().get_current_user_data_from_token()   
        return jsonify(claims), 200        

    #получение/заполнение формы с данными пользователя
    @check_auth
    @route("/setting/", methods=["GET", "POST"])
    def set_account(self):
        form = SettingsForm(request.form)
        uid, claims = get_auth_instance().get_current_user_data_from_token()
        if request.method == 'POST':
            #TODO: написать загрузку аватарки            
            
            if not form.validate():
                #в setting не забыть выводить сообщения об ошибке                
                return render_template('account/setting.html', form=form)

            if form.delete.data:
                return redirect('/delete/'), 303
                       
            user = User.query.filter_by(id = uid).first()
            user.nickname = form.nickname.data
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.email = form.email.data
            user.telegram_nickname = form.telegram_nickname.data
            db.session.commit()
            
            return redirect('/setting/'), 303

        form.nickname = claims['nickname']
        form.first_name = claims['first_name']
        form.last_name = claims['last_name']
        form.email = claims['email']
        form.telegram_nickname = claims['telegram_nickname']

        return render_template('account/setting.html', form = form)   

    #удаление аккаунта пользователя с сообщением о причине
    @check_auth
    @route('/delete/', methods=["GET", "POST"])
    def delete_account(self):
        form = DeleteFeedback(request.form)

        if request.method == 'POST':

            if not form.validate():
                return render_template("account/delete.html", form=form)

            user_message = form.message.data
            uid, claims = get_auth_instance().get_current_user_data_from_token()   
                     
            msg = Message("Сообщение об удалении аккаунта пользователем %s" % claims['nickname'],
                recipients=['justbeginnoreply@gmail.com'])
            msg.body = user_message
            mail.send(msg)

            user = User.query.filter_by(id = uid).first()
            db.session.delete(user)
            db.session.commit()

            return redirect("/home/"), 303
        return render_template("account/delete.html", form=form)


Account.register(bp)




