from django.contrib import admin
from .models import Category, Product


# функция обнуления товара на складе
def nullify_quantity(modeladmin,
                     # request — объект хранящий информацию о запросе
                     request,
                     # queryset — набор выделяемых объектов.
                     queryset):
    queryset.update(quantity=0)


# описание для более понятного представления в админ панели
nullify_quantity.short_description = 'Nullify products quantity'


# создаём новый класс для представления товаров в админке
class ProductAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые будут в таблице с товарами
    list_display = ('name', 'price', 'on_stock')  # оставляем только имя, цену и свойство 'on_stock'
    list_filter = ('price', 'quantity', 'name')  # простой фильтр для админки
    search_fields = ('name', 'category__name')  # поиск по имени и категории
    actions = [nullify_quantity]  # добавляем действия в список


# регистрируем модели (подтягиваем в админку)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)  # добавляем вновь созданный класс к модели
