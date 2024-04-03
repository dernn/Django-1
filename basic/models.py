from django.db import models
from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy  # импортируем «ленивый» геттекст с подсказкой


class Category(models.Model):
    name = models.CharField(max_length=100,
                            help_text=_('Category name'))  # добавим переводящийся текст подсказку к полю


class MyModel(models.Model):
    name = models.CharField(max_length=100)
    kind = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='kinds',
        # 'pgettext_lazy(context, message)' take a context string as the first variable
        help_text=pgettext_lazy('help text for MyModel model', 'This is the help text'),
    )
