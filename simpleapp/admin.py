from django.contrib import admin
from .models import Category, Product

# регистрируем модели (подтягиваем в админку)
admin.site.register(Category)
admin.site.register(Product)
admin.site.unregister(Product)  # разрегистрируем наши товары
