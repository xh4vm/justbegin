from flask import render_template, request, jsonify, redirect
from flask_jwt_extended import get_jwt_claims, jwt_optional, get_jwt_identity, get_raw_jwt
from flask_classy import FlaskView, route
from app.home import bp
from .exceptions import HomeExceptions


class Home(FlaskView):
    pass

@bp.route('/', methods=['GET'])
def index_view():
    return redirect('/home/', code=303)

Home.register(bp)
