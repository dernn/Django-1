from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
# импортируем функцию для перевода
from django.utils.translation import gettext as _


class Index(View):
    def get(self, request):
        string = _('Hello world')

        context = {
            'string': string
        }

        return HttpResponse(render(request, 'basic/index.html', context))