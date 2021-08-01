from app import db
from app.decorators import request_is_json
from flask import json, render_template, request, jsonify, redirect, current_app
from flask_classy import FlaskView, route
from app.project import bp
from app.auth.responses import *
import jwt


class Comments(FlaskView):

    def get(self):
        pass

Comments.register(bp, route_prefix='/projects/')
