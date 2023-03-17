"""todos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
]
