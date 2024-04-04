from datetime import datetime

from django.core.cache import cache  # импортируем наш кэш
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product
from pprint import pprint

# from D7
from .filters import ProductFilter  # импортируем недавно написанный фильтр (D7.2)
from .forms import ProductForm  # импортируем нашу форму (D7.3)


# из списка на главной странице уберём всё лишнее
class ProductsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Product
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-price'

    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'simpleapp/products.html'

    # Это имя списка, в котором будут лежать все объекты ('products').
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'products'  # по умолчанию носит имя 'object_list' и 'form'(?)
    paginate_by = 2  # поставим постраничный вывод в два элемента

    # Метод get_context_data позволяет нам изменить набор данных, который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам. В ответе мы должны получить {словарь}.

        # Забираем отфильтрованные объекты, переопределяя метод get_context_data у наследуемого класса
        context = super().get_context_data(**kwargs)  # сначала переопределяем набор аргументов класса
        # Затем вписываем наш фильтр в контекст
        context['filter'] = ProductFilter(self.request.GET, queryset=self.get_queryset())

        # Зачем здесь это? Просто чтобы видеть GET-параметры в контексте?
        try:
            context['parameter'] = context['filter'].data.urlencode()
        except AttributeError:
            pass

        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.now()
        # после добавления тега 'current_time' передавать в контекст datetime.now() больше нет необходимости

        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_sale'] = None
        # context['next_sale'] = 'Wednesday Sale!'
        pprint(context)  # вывод всего содержимого объекта (context) в консоль
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        # здесь возвращается queryset, к которому в шаблоне уже можно обратиться
        # через context_object_name класса ProductsList ('products')
        return ProductFilter(self.request.GET, queryset=queryset).qs


# дженерик для получения деталей о товаре
class ProductDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Product
    # Используем другой шаблон — product_detail.html
    template_name = 'simpleapp/product_detail.html'

    # здесь context_object_name уже 'product' [см. pprint(context)]
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pprint(context)
        return context

    # for D11.4: The low-level cache API
    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта
        obj = cache.get(f'product-{self.kwargs["pk"]}',
                        None)
        # Кэш очень похож на словарь, и метод get действует так же.
        # Он забирает значение по ключу, а если его нет, то забирает None.

        # Если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs["pk"]}', obj)

        return obj


# Дженерик для создания объекта.
# Надо указать только имя шаблона и класс формы, который мы
# написали в прошлом юните (D7.3). Остальное он сделает за нас.
class ProductCreate(CreateView):
    template_name = 'simpleapp/product_create.html'
    form_class = ProductForm  # передаём модельную форму в атрибут, чтобы получать доступ к форме через метод POST

    # здесь context_object_name уже 'form' [см. pprint(context)]
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pprint(context)
        return context


# дженерик для редактирования объекта
class ProductUpdate(UpdateView):
    template_name = 'simpleapp/product_create.html'
    form_class = ProductForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте,
    # который мы собираемся редактировать (все вызовы методов происходят "под капотом")
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Product.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pprint(context)
        return context


# дженерик для удаления товара
class ProductDelete(DeleteView):
    template_name = 'simpleapp/product_delete.html'
    queryset = Product.objects.all()
    model = Product
    success_url = '/products/'
