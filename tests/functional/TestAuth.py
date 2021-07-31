from flask import request
from flask.globals import current_app
from flask_jwt_extended import decode_token
from datetime import datetime


class TestAuth:
    def get_header_set_cookie(self, response):
        return response.headers.get('Set-Cookie')
        
    def get_set_cookie_name(self, response):
        return response.headers.get('Set-Cookie').split('=')[0]

    def get_token(self, response):
        return response.headers.get('Set-Cookie').split('=')[1].split(';')[0]

    def get_jwt_claims(self, response):
        token = self.get_token(response)
        return decode_token(token)['user_claims']

    def get_jwt_identity(self, response):
        token = self.get_token(response)
        return decode_token(token)['identity']

    def get_jwt_exp(self, response):
        token = self.get_token(response)
        return decode_token(token)['exp']  

    def verify_exp_jwt(self, response):
        exp = self.get_jwt_exp(response)
        return exp > datetime.now().timestamp()

    def get_cookie(self, cookie_name):
        return request.cookies.get(cookie_name)