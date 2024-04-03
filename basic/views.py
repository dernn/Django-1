from django.http import HttpResponse
from django.views import View
# импортируем функцию для перевода
from django.utils.translation import gettext as _


class Index(View):
    def get(self, request):
        string = _('Hello world')

        return HttpResponse(string)
