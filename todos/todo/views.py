from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm # Создаем форму входа в личный кабинет


def signupuser(request):
    return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})

def currenttodos(request):
    return render(request, 'todo/currenttodos.html')

