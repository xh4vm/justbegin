


from app.utils.request_type import IRequestType
from flask import request


class JSON(IRequestType):

    def get(self) -> dict:
        return request.json