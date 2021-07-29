from abc import ABCMeta, abstractmethod


class IAuth:
    __metaclass__ = ABCMeta

    @abstractmethod
    def sign_in(self, email, password):
        '''Авторизация в сервисе'''

    @abstractmethod
    def sign_up(self, data):
        '''Регистрация нового пользователя в сервисе'''

    @abstractmethod
    def reset_password(self, email):
        '''Сброс пароля пользователя'''
    
