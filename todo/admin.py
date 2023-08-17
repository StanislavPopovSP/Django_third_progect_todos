from django.contrib import admin
from .models import Todo


class TodoAdmin(admin.ModelAdmin): # Хотим увидеть дату создания задачи в Админке
    readonly_fields = ('created',) # Данные переменные уже есть, мы наследуем их и переопределяем поле. Переменная должна принимать либо кортеж, либо список.


admin.site.register(Todo, TodoAdmin) # Это что бы в админке видели текущую модель