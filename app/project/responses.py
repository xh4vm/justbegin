from app.responses import DefaultResponses
from string import Template


class ProjectResponses(DefaultResponses):
    BAD_PROJECT_ID_DATA = {"status": "fail", "message": "Неверный идентификатор проекта."}
    IS_NOT_PROJECT_ADMIN = {"status": "fail", "message": "Пользователь не является основателем проекта."}
    SUCCESS_REMOVE = {'status': 'success', 'message': Template('Проект $title был успешно удален.')}

    