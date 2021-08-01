from app.auth.methods import IAuth
from app.utils.MetaSingleton import MetaSingleton


class Authentificator(metaclass=MetaSingleton):
    def __init__(self, auth_method: IAuth) -> None:
        self.auth_method = auth_method

    def set_auth_method(self, auth_method: IAuth) -> None:
        self.auth_method = auth_method

    def get_auth_method(self) -> object:
        return self.auth_method
    
    def get_instance(self) -> IAuth:
        return self.auth_method.__call__()