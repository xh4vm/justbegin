from app import db
from flask import redirect, request, render_template
from flask_classy import FlaskView, route
from app.account import bp
from app.decorators import check_auth
from app.auth.utils import get_auth_instance
from app.models import User
from app.account.forms import SettingsForm, DeleteFeedback

class Account(FlaskView):

    @check_auth
    def get(self):
        id, claims = get_auth_instance().get_current_user_data_from_token()        
        return render_template("account/index.html", user = claims), 200

    @check_auth
    @route("/setting/", methods=["GET", "POST"])
    def set_account(self):
        uid, claims = get_auth_instance().get_current_user_data_from_token()
        if request.method == "POST":     
            #TODO: написать загрузку аватарки
            form = SettingsForm()

            if not form.validate_on_submit():
                #в setting не забыть выводить сообщения об ошибке
                return render_template("account/setting.html", form=form)

            if form.delete.data:
                return redirect("/delete", 302)

            user = User.query.filter_by(id = uid).first()
            user.nickname = form.nickname.data
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.email = form.email.data
            user.telegram_nickname = form.telegram_nickname.data
            db.session.commit()
            
            return redirect("/setting", 302)

        return render_template("account/setting.html", user = claims)   

    @check_auth
    @route('/delete/', methods=["GET", "POST"])
    def delete_account(self):
        form = DeleteFeedback()

        if not form.validate_on_submit():
            return render_template("account/delete.html", form=form)

        #куда сохраняем сообщение?
        message = form.message.data
        uid, claim = get_auth_instance().get_current_user_data_from_token()

        user = User.query.filter_by(id = uid).first()
        db.session.delete(user)
        db.session.commit()

        return redirect("/home/", 302)


Account.register(bp)




