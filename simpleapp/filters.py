# python -m pip install django-filter
# settings.py --> INSTALLED_APPS.append(filters.py)
# и создать файл filters.py в директории simpleapp/

from django_filters import FilterSet  # импортируем FilterSet, чем-то напоминающий знакомые дженерики
from .models import Product


# создаём фильтр
class ProductFilter(FilterSet):
    # Здесь в мета классе надо предоставить модель и указать поля,
    # по которым будет фильтроваться (т. е. подбираться) информация о товарах
    class Meta:
        model = Product
        # поля, которые мы будем фильтровать (т. е. отбирать по каким-то критериям, имена берутся из моделей)
        fields = {
            # мы хотим чтобы нам выводило имя хотя бы отдалённо похожее на то, что запросил пользователь
            'name': ['icontains'],
            # цена должна быть меньше или равна тому, что указал пользователь
            'price': ['lt'],
            # количество товаров должно быть больше или равно тому, что указал пользователь
            'quantity': ['gt'],
            'category': ['exact'],
        }
