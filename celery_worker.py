from app import create_app, celery, make_celery


app = create_app()
make_celery(app)

## Добавляем задачи для сельдерея сюда 
# например: from app.structure import Structure