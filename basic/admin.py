from django.contrib import admin
from basic.models import Category, MyModel
# импорт модели амдинки (переопределение стандартных админ-инструментов)
from modeltranslation.admin import TranslationAdmin


# Регистрируем модели для перевода в админке

class CategoryAdmin(TranslationAdmin):
    model = Category


class MyModelAdmin(TranslationAdmin):
    model = MyModel


# регистрируем модели (подтягиваем в админку)
admin.site.register(Category)
admin.site.register(MyModel)  # добавляем вновь созданный класс к модели
