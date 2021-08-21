


from app.utils.request_type import IRequestType
from flask import request


class Form(IRequestType):

    def get(self) -> dict:
        return request.form