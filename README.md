# Проект "Фудграм"

Проект представляет собой сайт, на котором пользователи могут публиковать свои рецепты, 
добавлять чужие рецепты в избранное и подписываться на публикации других авторов.
Помимо этого, пользователям доступен сервис "Список покупок", позволяющий создать список 
продуктов, которые нужно купить для приготовления выбранных блюд.
 
Проект доступен по адресу fooodgrammm.hopto.org
https://fooodgrammm.hopto.org/signin

### Данные для админки

```
e-mail: admin@mail.ru
login: admin
password: admin
```

## Как запустить проект

Клонировать репозиторий и перейти в папку бэкенда:
```
git clone git@github.com:Leonidx05/foodgram-project-react.git
```
cd foodgram-project-react/backend/
```

Создать и активировать виртуальное окружение:
```
python -m venv venv
```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
```
pip install -r requirements.txt
```

После установки зависимостей перейти в директорию с инфраструктурой и создать файл .env:

touch .env
```

Заполнить файл .env в соответствии с примером .env.example, размещенным в директории:

```
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_NAME=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=
ALLOWED_HOSTS=127.0.0.1,localhost,backend,0.0.0.0:8000
```

Запустить контейнеры локально следующей командой:
```
sudo docker compose up --build
```

После запуска, в другом терминале копировать статику бэкенда внутри контейнера:
```
sudo docker compose exec backend python manage.py collectstatic
```
sudo docker compose exec backend cp -r /app/static/. /backend_static/static
```

Там же создать и выполнить миграции:
```
sudo docker compose exec backend python manage.py makemigrations
```
```
sudo docker compose exec backend python manage.py migrate
```

Там же создать суперпользователя:
```
sudo docker compose exec backend python manage.py createsuperuser
```

После этого можно создать ингредиенты и теги войдя в админ-зону в роли суперпользователя:
```
http://localhost:8000/admin/
```

Затем проект станет доступен локально по адресу:
```
http://localhost:8000/
```