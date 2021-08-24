# from app.user.decorators import check_auth, user_exists, user_required
from flask import request, jsonify
from flask_classy import FlaskView, route
from sqlalchemy.orm.scoping import scoped_session
from app import db
from .exceptions import ChatExceptions
# from app.user.model import User
# from .models import Chat, ChatParty, ChatMessage, ChatMessageStatus


class Chats(FlaskView):
    session : scoped_session = db.session

    # @user_required
    @route('/', methods=['GET'])
    def get_chats(self):
        pass