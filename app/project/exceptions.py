from app.exceptions import DefaultExceptions


class ProjectExceptions(DefaultExceptions):
    BAD_PROJECT_ID_DATA = {"status": "fail", "message": "Неверный идентификатор проекта."}
    IS_NOT_PROJECT_ADMIN = {"status": "fail", "message": "Пользователь не является основателем проекта."}

    