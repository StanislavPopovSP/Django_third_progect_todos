from django.contrib import admin
from django.urls import path
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('signup/', views.signupuser, name='signupuser'), # страница для входа в личный кабинет
    path('login/', views.loginuser, name='loginuser'), # Реализуем авторизацию пользователя в личный кабинет.
    path('logout/', views.logoutuser, name='logoutuser'), # путь для кнопки выхода

    # Todos
    path('', views.home, name='home'), # После выхода(когда разлогинились) перенаправит на гланую страницу
    path('current/', views.currenttodos, name='currenttodos'), # Наши задачи
    path('create/', views.createtodo, name='createtodo'), # Путь для создания задачи
    path('todo/<int:todo_pk>/', views.viewtodo, name='viewtodo'), # путь конкретной записи, указываем int - должем быть числовым значением, в виде ключа todo_pk(это id которое будет приходить в функцию вторым параметром). (Для перехода на конкретный путь выбранной задачи)
    path('todo/<int:todo_pk>/complete', views.completetodo, name='completetodo'), # путь для создания какой-то выполненной задачи.
    path('todo/<int:todo_pk>/delete', views.deletetodo, name='deletetodo'),
    path('completed/', views.completedtodo, name='completedtodo'),
]
