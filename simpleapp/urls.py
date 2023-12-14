from django.urls import path
# Импортируем созданные нами представления
from .views import ProductsList, ProductDetail, Products, ProductCreate, ProductUpdate, ProductDelete

urlpatterns = [
    # path — означает путь.
    # В данном случае путь ко всем товарам у нас останется пустым,
    # чуть позже станет ясно почему.
    # Т.к. наше объявленное представление является классом,
    # а Django ожидает функцию, нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.
    path('', ProductsList.as_view()),
    path('custom/', Products.as_view()),
    # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    # int — указывает на то, что принимаются только целочисленные значения
    path('<int:pk>/', ProductDetail.as_view(), name='product_detail'),  # Ссылка на детали товара
    path('create/', ProductCreate.as_view(), name='product_create'),  # Ссылка на создание товара
    path('update/<int:pk>', ProductUpdate.as_view(), name='product_update'),  # Ссылка на редактирование
    path('delete/<int:pk>', ProductDelete.as_view(), name='product_delete'),  # Ссылка на создание товара
]
