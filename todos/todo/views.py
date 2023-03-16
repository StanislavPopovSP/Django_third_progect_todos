from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  # Создаем форму входа в личный кабинет, а затем форму аутентификации.
from django.contrib.auth.models import User  # Возможность регистрации, User - это таблица в БД.
from django.contrib.auth import login, logout, authenticate  # Нужно пользователя залогинить, затем что бы вышел(разлогиниться), после этого аутентификация(Авторизация).
from django.db import IntegrityError  # Для exept импортируем модуль
from .forms import TodoForm


def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    """Функция, регистрации пользователя"""
    if request.method == 'GET':  # Если GET, то получили доступ к странице
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})  # UserCreationForm() - вызываем как функцию
    else:
        if request.POST['password1'] == request.POST['password2']:  # Хотим создавать нового пользователя. Мы сравним пароли на совпадение.
            try:  # Если все хорошо
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])  # будем создавать пользователя, в user положим экземпляр как класса User кот-го импортировали из django. .objects - из БД берем метод create_user(), гот-й метод. В create_user нужно передать что мы хотим записать в БД. Что бы пароль не записался в email второй параметр будет именованный.
                user.save()  # Нам нужно, что бы эти данные сохранились в БД
                login(request, user)  # После сохранения пользователя в БД, логиним пользователя.
                return redirect('currenttodos')  # И укажем страницу куда нужно перенаправить пользователя после того как зарегистрировался. В данном случае на страничку с задачами.
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {
                    'form': UserCreationForm(),
                    'error': 'Такое имя пользователя уже существует. Задайте другое имя'
                })  # Укажем на какую страницу нас будет переадресовывать, если пойдет что-то не так, нужно указать снова переменную, что бы на странице была сама форма. Кроме этого создадим еще ошибку 'error'.
        else:
            return render(request, 'todo/signupuser.html', {
                'form': UserCreationForm(),
                'error': 'Пароли не совпадают'
            })  # Если не совпали пароли


def loginuser(request):
    if request.method == 'GET':  # Метод GET - это если мы зайдем на эту страницу
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:  # Пропишем авторизацию пользователя
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])  # вторым параметром передаем по каким полям мы будем аутентифицироваться, передаем именованные значения.
        # А что будет если пользователя в БД с таким именем нету
        if user is None:
            return render(request, 'todo/loginuser.html',
                          {'form': AuthenticationForm(),
                           'error': 'Неверные данные для входа'
                           })  # Тогда мы пользователя должны перенаправить на страницу входа назад
        else:
            login(request, user)  # если пользователь есть, login() - он должен быть авторизирован, проверка на то что он есть
            return redirect('currenttodos')  # переведем его на задачи


def logoutuser(request):
    if request.method == 'POST':  # Метод POST может быть только у элемента form
        logout(request)
        return redirect('home')  # Куда мы должны перейти когда разлогинились


def currenttodos(request):
    return render(request, 'todo/currenttodos.html')


def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form': TodoForm()}) # TodoForm() - вызовем как экземпляр класса
    else:
        try:
            form = TodoForm(request.POST) # В переменную form запишутся данные которые получены будут методом POST из формы TodoForm.
            new_todo = form.save(commit=False) # сохраняем данные которые ввел пользователь. commit=False - это значит что он сохраняет данные в БД.
            new_todo.user = request.user # нужно сохранить данные привязанные к пользователю. Укажем что бы сохранял данные, того пользователя, который заполнял это поле авторизированный на сайте. Какой именно пользователь эти данные создал.
            new_todo.save() # Так же данные эти нужно сохранить
            return redirect('currenttodos') # Перенаправляем пользователя, на все задачи которые сущ-ют
        except ValueError: # Это наши вводимые значения
            return render(request, 'todo/createtodo.html', {
                           'form': TodoForm(),
                           'error': 'Переданы неверные данные. Попробуйте еще раз.'
                          })