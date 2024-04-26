from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from basic.models import MyModel

from django.utils import timezone
from django.shortcuts import redirect

import pytz  # импортируем стандартный модуль для работы с часовыми поясами


class Index(View):
    def get(self, request):
        # Translators: This message appears on the home page only
        models = MyModel.objects.all()

        context = {
            # передаём всё объекты модели в контекст
            'models': models,
            'available_languages': ['en', 'ru'],
            'current_time': timezone.localtime(),  # returns datetime in the selected time zone
            'timezones': pytz.common_timezones  # добавляем все доступные часовые пояса
        }

        return HttpResponse(render(request, 'basic/index.html', context))

    #  по пост-запросу будем добавлять в сессию часовой пояс, который и будет обрабатываться кастомным middleware
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')
