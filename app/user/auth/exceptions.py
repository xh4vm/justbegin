from app.exceptions import DefaultExceptions


class AuthExceptions(DefaultExceptions):
    ALREADY_AUTH = {"message": "Авторизация уже была произведена вами ранее."}
    BAD_AUTH_DATA = {"message": "Неверный логин или пароль."}
    BAD_CONFIRM_PASSWORD = {'message': "Пароли не совпадают."}
    DUPLICATE_EMAIL = {'message': "Пользователь на данную почту уже зарегистрирован."}
    UNKNOWN_USER = {'message': "Не найден указанный пользователь."}
    RESET_TOKENT_EXPIRED = {'message': "Истекло время действия одноразового токена для сброса пароля."}
