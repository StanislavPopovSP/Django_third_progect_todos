<h2 align="center">Todos</h2>


### Описание проекта:
Приложение список дел.

Приложение позволяет создать задачи для пользователя, отредактировать, перевести в статус выполнено или удалить,
а также сделать ее важной или нет. Так же пользователь может увидеть свои выполненные задачи.

### Функционал

- Авторизация, регистрация через форму
- Задачу можно
    - Создать
    - Изменить
    - Удалить
    - Сделать важной
    - Поставить как выполненную
- Посмотреть актуальную задачу и выполненную

### Инструменты разработки

**Стек:**
- Python >= 3.9
- Django == 4.2
- sqlite3

## Установка

##### 1) Клонировать репозиторий

    https://github.com/StanislavPopovSP/Django_third_progect_todos.git

##### 2) Создать виртуальное окружение

    python -m venv venv

##### 3) Активировать виртуальное окружение

Linux

    source venv/bin/activate

Windows

    ./venv/Scripts/activate

##### 4) Устанавливить зависимости:

    pip install -r requirements.txt

##### 5) Выполнить команду для выполнения миграций

    python manage.py migrate

##### 6) Создать суперпользователя

    python manage.py createsuperuser

##### 7) Запустить сервер

    python manage.py runserver

##### 8) Ссылки

- Сайт http://127.0.0.1:8000/

- Админ панель http://127.0.0.1:8000/admin
