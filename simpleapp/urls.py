from django.urls import path
# Импортируем созданные нами представления
from .views import ProductsList, ProductDetail, ProductCreate, ProductUpdate, ProductDelete

urlpatterns = [
    # path — означает путь.
    # В данном случае путь ко всем товарам у нас останется пустым,
    # чуть позже станет ясно почему.
    # Так как наше объявленное представление является классом,
    # а Django ожидает функцию, нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.
    path('', ProductsList.as_view()),

    # Добавим кэширование на детали товара.
    # Раз в 10 минут товар будет записываться в кэш для экономии ресурсов.
    path('<int:pk>/', ProductDetail.as_view(), name='product_detail'),
    path('create/', ProductCreate.as_view(), name='product_create'),  # Ссылка на создание товара
    path('update/<int:pk>', ProductUpdate.as_view(), name='product_update'),  # Ссылка на редактирование
    path('delete/<int:pk>', ProductDelete.as_view(), name='product_delete'),  # Ссылка на создание товара
]
