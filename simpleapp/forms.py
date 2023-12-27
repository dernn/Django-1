from django.forms import ModelForm, BooleanField  # Импортируем true-false поле
from .models import Product


# Создаём модельную форму
class ProductForm(ModelForm):
    check_box = BooleanField(label='Confirm!')  # добавляем галочку, или же true-false поле

    # в класс мета, как обычно, надо написать модель, по которой будет строиться форма и нужные нам поля.
    # Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = Product
        fields = ['name', 'price', 'quantity', 'category',
                  # в юните D7.3 предлагают включать галочку в поля мета-класса, иначе она не будет отображаться,
                  # однако на практике поле подтягивается из класса ProductForm без этого
                  # 'check_box',
                  ]
