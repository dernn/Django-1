from basic.models import Category, MyModel
# импорт декоратора перевода и класса настроек, от которого будем наследоваться
from modeltranslation.translator import register, TranslationOptions


# регистрируем наши модели для перевода

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)  # указываем, какие именно поля надо переводить в виде кортежа


@register(MyModel)
class MyModelTranslationOptions(TranslationOptions):
    fields = ('name',)
