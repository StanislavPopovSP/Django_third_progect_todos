from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm # Создаем форму входа в личный кабинет
from django.contrib.auth.models import User # Возможность регистрации


def signupuser(request):
    return render(request, 'todo/signupuser.html', {'form': UserCreationForm()}) # UserCreationForm() - вызываем как функцию

def currenttodos(request):
    return render(request, 'todo/currenttodos.html')

