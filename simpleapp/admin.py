from django.contrib import admin
from .models import Category, Product


# создаём новый класс для представления товаров в админке
class ProductAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые будут в таблице с товарами
    list_display = [field.name for field in
                    Product._meta.get_fields()]  # генерируем список имён всех полей для более красивого отображения


# регистрируем модели (подтягиваем в админку)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)  # добавляем вновь созданный класс к модели
