import os
import datetime
from django.http import HttpResponse
from django.shortcuts import render, reverse


def home_view(request):
    template_name = 'app/home.html'
    # впишите правильные адреса страниц, используя
    # функцию `reverse`
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir')
    }
    
    # context и параметры render менять не нужно
    # подбробнее о них мы поговорим на следующих лекциях
    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    # обратите внимание – здесь HTML шаблона нет, 
    # возвращается просто текст
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f'Текущее время: {current_time}'
    return HttpResponse(msg)


def workdir_view(request):
    # Получаем список файлов и директорий в текущей папке ('.')
    files = os.listdir('.')

    # Для красивого вывода в браузере объединим список через тег переноса строки <br>
    # Можно также использовать HTML-список, но этот способ проще и надёжнее
    files_formatted = "<br>".join(files)

    msg = f"Содержимое рабочей директории:<br><br>{files_formatted}"
    return HttpResponse(msg)
