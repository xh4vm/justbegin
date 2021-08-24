from app.exceptions import DefaultExceptions


class AuthExceptions(DefaultExceptions):
    ALREADY_AUTH = {"status": "fail", "message": "Авторизация уже была произведена вами ранее."}
    BAD_AUTH_DATA = {"status": "fail", "message": "Неверный логин или пароль."}
    BAD_CONFIRM_PASSWORD = {'status': 'fail', 'message': "Пароли не совпадают."}
    DUPLICATE_EMAIL = {'status': 'fail', 'message': "Пользователь на данную почту уже зарегистрирован."}
    UNKNOWN_USER = {'status': 'fail', 'message': "Не найден указанный пользователь."}
    RESET_TOKENT_EXPIRED = {'status': 'fail', 'message': "Истекло время действия одноразового токена для сброса пароля."}
