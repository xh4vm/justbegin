from abc import ABCMeta, abstractmethod


class IAuth:
    __metaclass__ = ABCMeta

    @abstractmethod
    def sign_in(self, email: str, password: str) -> object:
        '''Авторизация в сервисе'''

    @abstractmethod
    def sign_up(self, data: object) -> object:
        '''Регистрация нового пользователя в сервисе'''

    @abstractmethod
    def reset_password(self, email: str) -> object:
        '''Сброс пароля пользователя'''

    @abstractmethod
    def logout(self) -> object:
        '''Выход'''
    
