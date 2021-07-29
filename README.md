# JustBegin

Надеюсь проект будет носить гордое клеймо стартапа, а его создатели смогут сделать мир вокруг ярче, а свою жизнь лучше!

## Для запуска выполнить следующие действия:
```
docker-compose up -d --build  
```
Теперь в браузере по ссылке http://localhost:8000 будет транслироваться наш проект

## Для запуска тестов:
```
docker exec -it justbegin_web_1 pytest -vv --cov=app/ 
```

## Для обновления структуры базы данных:
```
docker exec -it justbegin_web_1 flask db migrate && flask db upgrade
```
