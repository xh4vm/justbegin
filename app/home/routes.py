from flask import render_template, request, jsonify, redirect
from flask_jwt_extended import get_jwt_claims, jwt_optional, get_jwt_identity, get_raw_jwt
from flask_classy import FlaskView, route
from app.home import bp
from app.home.responses import HomeResponses


class Home(FlaskView):

    @route('/', methods=['GET'])
    @jwt_optional
    def index_home_view(self):
        return HomeResponses.INDEX_SUCCESS, 200

@bp.route('/', methods=['GET'])
def index_view():
    return redirect('/home/', code=302)

Home.register(bp)
