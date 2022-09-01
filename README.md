# QRkot_spreadseets
Формирование отчёта в гугл-таблице. 
В таблице находятся закрытые проекты, отсортированные по скорости сбора средств — от тех, 
что закрылись быстрее всего, до тех, что долго собирали нужную сумму.

https://github.com/Anzhela-Namistyuk/QRkot_spreadsheets/main/QRkot_spreadsheets/image/google_table.png

### Приложение для Благотворительного фонда QRKot
Фонд собирает пожертвования на различные целевые проекты
связанные с поддержкой кошачьей популяции.
У каждого проекта есть название, описание и сумма, которую планируется собрать. 
После того, как нужная сумма собрана — проект закрывается.
Каждый пользователь может сделать пожертвование и сопроводить его комментарием.
Пожертвования не целевые: они вносятся в фонд, а не в конкретный проект.


### Технологии.
```
Python 3,  SQLite3, SQLAlchemy, Alembic, pydantic, asyncio
```

#### Шаблон наполнения env-файла.

APP_TITLE=Благотворительный фонд поддержки котиков QRKot (название приложения)
DESCRIPTION=Фонд собирает пожертвования на любые цели,
связанные с поддержкой кошачьей популяции (описание приложения)
DATABASE_URL=sqlite+aiosqlite:///./name_data_base.db (путь и название до базы данных)
SECRET = secret

Клонировать репозиторий и перейти в него в командной строке:

```
git clone 
```

```
cd  cat_charity_fund
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/MacOS

```
source venv/bin/activate
```

* Если у вас windows

 ```
source venv/scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Команда для автоматического создания файла миграции

```
alembic revision --autogenerate -m "First migration" 
```

Выполнение всех неприменённых миграций запускается командой

```
alembic upgrade head 
```


Запустить приложение 

```
uvicorn app.main:app --reload 

```
Пример POST запроса на http://127.0.0.1:8000/charity_project/

Запрос

```
{
  "name": "Feed the cats",
  "description": "for homeless cats",
  "full_amount": 150
}
```

Ответ

```
{
  "name": "Feed the cats",
  "description": "for homeless cats",
  "full_amount": 150
  "id": 0,
  "invested_amount": 150,
  "fully_invested": true,
  "create_date": "2022-08-12T14:49:38.927Z",
  "close_date": "2022-08-12T14:49:38.927Z"
}
```

Пример GET запроса на http://127.0.0.1:8000/charity_project/

Ответ

```
[
  {
    "name": "Feed the cats",
    "description": "for homeless cats",
    "full_amount": 150
    "id": 0,
    "invested_amount": 150,
    "fully_invested": true,
    "create_date": "2022-08-04T13:45:10.939988",
    "close_date": "2022-08-11T17:54:10.956223"
  },
  {
    "name": "Warm nurseries",
    "description": "help for cats nurseries",
    "full_amount": 5000,
    "id": 1,
    "invested_amount": 2600,
    "fully_invested": false,
    "create_date": "2022-08-06T15:43:42.159600",
    "close_date": null
  },
]
```


Пример POST запроса на 'http://127.0.0.1:8000/donation/'
```
{
  "full_amount": 500,
  "comment": "for food"
}
```
Ответ
```
{
  "full_amount": 500,
  "comment": "for food"
  "id": 0,
  "create_date": "2022-08-12T14:49:38.969Z"
}
```
Пример GET запроса на 'http://127.0.0.1:8000/donation/my'
```
[
  {
    "full_amount": 500,
    "comment": "for food"
    "id": 0,
    "create_date": "2022-08-12T14:49:38.969Z"
  },
  {
    "full_amount": 900,
    "comment": "on medicines"
    "id": 1,
    "create_date": "2022-09-12T16:46:30.678Z"
  }
]
```

Пример GET запроса на 'http://127.0.0.1:8000/donation/'

```
[
  {
    "full_amount": 500,
    "comment": "for food",
    "id": 0,
    "user_id": 1,
    "invested_amount": 500,
    "fully_invested": true,
    "create_date": "2022-08-12T14:49:38.969Z"
  },
  {
    "full_amount": 900,
    "comment": "on medicines",
    "id": 1,
    "user_id": 1,
    "invested_amount": 400,
    "fully_invested": false,
    "create_date": "2022-09-12T16:46:30.678Z"
  }
] 
```
GET запроса на 'http://127.0.0.1:8000/google/'
```
[
{
    "CharityProject": {
      "fully_invested": true,
      "id": 12,
      "close_date": "2022-08-16T10:52:55.383103",
      "description": "warm cover",
      "full_amount": 10000,
      "invested_amount": 10000,
      "create_date": "2022-08-16T10:50:41.160525",
      "name": "for sleep"
    }
  },
  {
    "CharityProject": {
      "fully_invested": true,
      "id": 9,
      "close_date": "2022-08-13T23:05:34.630989",
      "description": "for homeless cats",
      "full_amount": 45,
      "invested_amount": 45,
      "create_date": "2022-08-13T23:02:55.886554",
      "name": "FOR CATS"
    }
  },
]
```

### Автор
Намистюк Анжела
