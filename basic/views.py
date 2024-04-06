from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from basic.models import MyModel


class Index(View):
    def get(self, request):
        # Translators: This message appears on the home page only
        models = MyModel.objects.all()

        context = {
            # передаём всё объекты модели в контекст
            'models': models,
            'available_languages': ['en', 'ru'],
        }

        return HttpResponse(render(request, 'basic/index.html', context))
