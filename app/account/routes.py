from ..utils.request_type.JSON import JSON
from flask.json import jsonify
from app import db
from flask import redirect, request
from flask_classy import FlaskView, route
from app.auth.decorators import check_auth
from app.decorators import request_validation_required
from app.auth.utils import get_auth_instance
from app.auth.models import User
from app import mail
from flask_mail import Message
from .schemas import post_settings_schema, post_delete_account_schema
from werkzeug.utils import secure_filename

class Account(FlaskView):
    
    UPLOAD_FOLDER = '/path/to/upload'
    #получение данных пользователя
    @check_auth
    def get(self):
        uid, claims = get_auth_instance().get_current_user_data_from_token()   
        avatar = User.query.filter_by(id = uid).first().avatar

        result = claims
        result['avatar'] = avatar

        return jsonify(result), 200        


    @check_auth
    @request_validation_required(post_settings_schema, JSON)
    @route('/settings/', methods=['POST'])
    def post_settings(self, validated_request: dict):        
        uid, claims = get_auth_instance().get_current_user_data_from_token()       

        #file = request.files['file']
        #filename = secure_filename(file.filename)
        #file.save(os.path.join(self.UPLOAD_FOLDER, filename))

        user = User.query.filter_by(id = uid).first()
        user.nickname = validated_request.get('nickname')
        user.first_name = validated_request.get('first_name')
        user.last_name = validated_request.get('last_name')
        user.email = validated_request.get('email')
        user.telegram_nickname = validated_request.get('telegram_nickname')
        user.avatar = validated_request.get('avatar')
        db.session.commit()

        return redirect('/settings/'), 303


    @check_auth
    @route('/settings/', methods=['GET'])
    def get_settings(self):
        uid, claims = get_auth_instance().get_current_user_data_from_token()
        avatar = User.query.filter_by(id = uid).first().avatar

        result = claims
        result['avatar'] = avatar

        return jsonify(result), 200


    #удаление аккаунта пользователя с сообщением о причине
    @check_auth  

    @request_validation_required(post_delete_account_schema, JSON)  
    @route('/delete/', methods=['POST'])
    def post_delete(self, validated_request: dict):
        uid, claims = get_auth_instance().get_current_user_data_from_token() 

        user_message = validated_request.get('user_message')
                                   
        msg = Message('Сообщение об удалении аккаунта пользователем %s' % claims['nickname'],
                recipients=['justbeginnoreply@gmail.com'])
        msg.body = user_message
        mail.send(msg)

        user = User.query.filter_by(id = uid).first()
        db.session.delete(user)
        db.session.commit()

        return redirect('/home/'), 303

    
    @check_auth
    @route('/delete/', methods=['GET'])
    def get_delete_page(self):
        uid, claims = get_auth_instance().get_current_user_data_from_token()

        return jsonify(nickname = claims['nickname']), 200
