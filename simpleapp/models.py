from django.core.cache import cache
from django.db import models
from django.core.validators import MinValueValidator


# Товар для нашей витрины
class Product(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,  # названия товаров не должны повторяться
    )
    description = models.TextField(
    )
    quantity = models.IntegerField(
        validators=[MinValueValidator(0, 'Quantity should be >= 0')],  # количество не может быть меньше 0
    )
    # поле категории будет ссылаться на модель категории
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='products',  # все продукты в категории будут доступны через поле products
    )
    price = models.FloatField(
        validators=[MinValueValidator(0.0)],
    )

    # def __str__(self):
    #     return f'{self.name.title()}: {self.description[:20]} ({self.price})'

    # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром (D7.4)
    def get_absolute_url(self):
        return f'/products/{self.id}'

    # for D11.4: переопределяем метод сохранения модели
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'product-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его


# Категория, к которой будет привязываться товар
class Category(models.Model):
    # названия категорий тоже не должны повторяться
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name.title()
