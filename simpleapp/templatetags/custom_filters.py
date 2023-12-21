from django import template

# Library: класс для регистрации тэгов и фильтров
register = template.Library()

CURRENCIES_SYMBOLS = {
    'rub': '₽',
    'usd': '$',
}


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
# по умолчанию имя фильтра носит название функции
# @register.filter(name='currency_rub'): так можно задать имя фильтра ('currency_rub')
def currency(value, code='rub'):
    """
    value: значение, к которому нужно применить фильтр
    code: код валюты
    """

    postfix = CURRENCIES_SYMBOLS[code]

    # Возвращаемое функцией значение подставится в шаблон.
    return f'{value} {postfix}'
