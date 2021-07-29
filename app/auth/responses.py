
class AuthResponses:
    ALREADY_AUTH = {"status": "success", "message": "Авторизация уже была произведена вами ранее."}
    BAD_DATA_TYPE = {"status": "fail", "message": "Некорректный тип данных."}
    BAD_AUTH_DATA = {"status": "fail", "message": "Неверный логин или пароль."}
    BAD_CONFIRM_PASSWORD = {'status': 'fail', 'message': "Пароли не совпадают."}
    DUPLICATE_EMAIL = {'status': 'fail', 'message': "Пользователь на данную почту уже зарегистрирован"}