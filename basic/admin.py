from django.contrib import admin
from basic.models import Category, MyModel

# регистрируем модели (подтягиваем в админку)
admin.site.register(Category)
admin.site.register(MyModel)  # добавляем вновь созданный класс к модели
