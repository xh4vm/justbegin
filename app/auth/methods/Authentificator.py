from app.auth.methods import IAuth
from app.utils.MetaSingleton import MetaSingleton


class Authentificator(metaclass=MetaSingleton):
    def __init__(self, auth_method: IAuth):
        self.auth_method = auth_method

    def set_auth_method(self, auth_method: IAuth):
        self.auth_method = auth_method
    
    def get_instance(self):
        return self.auth_method.__call__()