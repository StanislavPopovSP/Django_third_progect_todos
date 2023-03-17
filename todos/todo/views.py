from django.shortcuts import render, redirect, get_object_or_404 # когда мы обратимся к id строки кот-й нет, либо возвращается объект, либо ошибка 404.
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  # Создаем форму входа в личный кабинет, а затем форму аутентификации.
from django.contrib.auth.models import User  # Возможность регистрации, User - это таблица в БД.
from django.contrib.auth import login, logout, authenticate  # Нужно пользователя залогинить, затем что бы вышел(разлогиниться), после этого аутентификация(Авторизация).
from django.db import IntegrityError  # Для exept импортируем модуль
from .forms import TodoForm
from .models import Todo # имортируем модель Тodo для получения данных.
from django.utils import timezone


def home(request):
    """Функция, перехода на главную страницу"""
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
    """Функция, для авторизации пользователя"""
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
    """Функция, кнопки выхода из аккаунта"""
    if request.method == 'POST':  # Метод POST может быть только у элемента form
        logout(request)
        return redirect('home')  # Куда мы должны перейти когда разлогинились


def currenttodos(request): # Будем выводить задачи (словарь из todos)
    """Функция, для вывода задач"""
    todos = Todo.objects.filter(user=request.user, data_completed__isnull=True) # filter() - метод, который дает возможность сделать какую то выборку. user=request.user - для текущего пользователя(что бы видел только свои записи). data_completed__isnull=True - это мы после выполнения задачи даем возможность её удалить. Допускается data_completed со значением isnull.
    return render(request, 'todo/currenttodos.html', {'todos': todos})


def createtodo(request):
    """Функция, для заполнения формы пользователем"""
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


def viewtodo(request, todo_pk):
    """Функция, возвращает данные выбранной задачи пользователя, с возможностью ее редактирования"""
    todo = get_object_or_404(Todo, pk=todo_pk) # первым параметром функция берет класс модели, вторым pk(Primary key аналог id) то что приходит в принимаемый аргумент метода. get_object_or_404 - данная функция ограничивает числа которые есть, а не любые которые вводит пользователь(Получить объект или ошибку 404).
    if request.method == 'GET':
        form = TodoForm(instance=todo)# сделаем редактирование одной записи. instance=тодо - те данные которые получили из метода get_object_or_404, что бы она дальше передавались в форму.(Конкретный экземпляр) Из этой формы будут браться конретные данные по элементу.
        return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form})
    else:
        try: # Так как мы работаем с данными они у нас могут конкретно отработать, может быть какой то сбой.
            form = TodoForm(request.POST, instance=todo) # Данные будем отправлять и что бы данные были уже заполнены.
            form.save()
            return redirect('currenttodos')
        except ValueError: # Обработаем ошибку значения.
            return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form, 'error': 'Неверные данные'})


def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user) # точно так же будем получать элемент по id из модели Тодо, что бы задача была выполнена, надо что бы автор только мог это сделать.
    if request.method == 'POST':
        todo.data_completed = timezone.now() # автоматически будет заполняться поле текущие даты и времени, в случае выполнения задачи когда мы нажмём на определенную кнопку.
        todo.save()
        return redirect('currenttodos') # из currenttodos этот элемент будет изчезать