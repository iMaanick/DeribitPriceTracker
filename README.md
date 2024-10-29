# Документация
Документация api:


```
http://localhost:8000/docs
```


# Запуск проекта

1. Клонируйте репозиторий:

```
https://github.com/iMaanick/DeribitPriceTracker.git
```

2. При необходимости установить Poetry ```pip install poetry```

3. Запустить виртуальное окружение ```poetry shell```

4. Установить зависимости ```poetry install```


5. Добавьте файл .env и заполните его как в примере .example.env:

```
DATABASE_URI=sqlite+aiosqlite:///test.db
```
6. Выполните для создания таблиц

```
alembic upgrade head 
```

7. Для запуска выполните:
```
python -m app.deribit_client.main
uvicorn --factory app.main:create_app --host localhost --port 8000
```

# Функциональность

1. Клиент каждую минуту забирает с биржи текущую цену btc_usd и eth_usd, сохраняет в базу данных тикер валюты, текущую цену и время в
UNIX timestamp.
2. API для обработки сохраненных данных. API включает методы:
    1. Получение всех сохраненных данных по указанной валюте 
    2. Получение последней цены валюты 
    3. Получение цены валюты с фильтром по дате 

# О проекте
1. FastAPI для разработки RESTful API
2. SQLite в качестве базы данных
4. SQLAlchemy для работы с базой данных
5. Alembic для управления миграциями
8. Poetry для управления зависимостями