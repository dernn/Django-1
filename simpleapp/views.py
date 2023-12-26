# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from datetime import datetime

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# Дополнительно импортируем категорию, чтобы пользователь мог её выбрать
from .models import Product, Category
from pprint import pprint

# from D7
from django.shortcuts import render
from django.views import View  # импортируем простую вьюшку
from django.core.paginator import Paginator  # импортируем класс, позволяющий удобно осуществлять постраничный вывод
from .filters import ProductFilter  # импортируем недавно написанный фильтр (D7.2)
from .forms import ProductForm  # импортируем нашу форму (D7.3)


# из списка на главной странице уберём всё лишнее
class ProductsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Product
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-price'

    # Фильтр по цене + сортировка по имени
    # queryset = Product.objects.filter(price__gt=100).order_by(
    #     '-name'
    # )

    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'products.html'

    # Это имя списка, в котором будут лежать все объекты ('products').
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'products'  # по умолчанию носит имя 'object_list' и 'form'(?)
    paginate_by = 2  # поставим постраничный вывод в два элемента

    # form_class = ProductForm  # добавляем форм класс, чтобы получать доступ к форме через метод POST

    # Метод get_context_data позволяет нам изменить набор данных, который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам. В ответе мы должны получить словарь.

        # Забираем отфильтрованные объекты, переопределяя метод get_context_data у наследуемого класса (привет,
        # полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)  # сначала переопределяем набор аргументов класса
        # Затем вписываем наш фильтр в контекст
        context['filter'] = ProductFilter(self.request.GET, queryset=self.get_queryset())

        # добавляем категории в контекст
        # context['categories'] = Category.objects.all()
        # передаем форму в контекст
        # context['form'] = ProductForm()

        # Зачем здесь это? Просто чтобы видеть параметры GET в контексте?
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
        pprint(context['view'])
        print(type(context['view']))
        return context

    # переопределение метода отключаем за ненадобностью
    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса
    #     if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый товар
    #         form.save()
    #     return super().get(request, *args, **kwargs)

    # # «самопал»
    # def post(self, request, *args, **kwargs):
    #     # берём значения для нового товара из POST-запроса, отправленного на сервер
    #     name = request.POST['name']
    #     quantity = request.POST['quantity']
    #     category_id = request.POST['category']
    #     price = request.POST['price']
    #     description = '<content>'
    #     # создаём новый товар и сохраняем
    #     product = Product(name=name, quantity=quantity, category_id=category_id, price=price, description=description)
    #     product.save()
    #     return super().get(request, *args, **kwargs)  # отправляем пользователя обратно на GET-запрос.

    def get_queryset(self):
        queryset = super().get_queryset()
        # здесь возвращается queryset, к которому в шаблоне уже можно обратиться
        # через context_object_name ProductsList ('products')
        return ProductFilter(self.request.GET, queryset=queryset).qs


# дженерик для получения деталей о товаре
class ProductDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Product
    # Используем другой шаблон — product_detail.html
    template_name = 'product_detail.html'

    # Название объекта, в котором будет выбранный пользователем продукт
    # context_object_name = 'product'

    # Возвращает <Queryset> всех объектов модели, но зачем он здесь?
    # queryset = Product.objects.all()

    # Переименование ссылки на первичный ключ
    # pk_url_kwarg = 'id'

    # замена для context_object_name = 'product' ?
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pprint(context)
        # pprint(ProductDetail)
        return context


# Дженерик для создания объекта
# Надо указать только имя шаблона и класс формы, который мы написали в прошлом юните. Остальное он сделает за вас
class ProductCreate(CreateView):
    template_name = 'product_create.html'
    form_class = ProductForm  # передаём модельную форму в атрибут, чтобы получать доступ к форме через метод POST

    # context_object_name = 'create'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pprint(context)

        return context


# дженерик для редактирования объекта
class ProductUpdate(UpdateView):
    template_name = 'product_create.html'
    form_class = ProductForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте,
    # который мы собираемся редактировать
    # все вызовы методов происходят "под капотом"
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Product.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pprint(context)
        pprint(context['view'])
        print(type(context['view']))
        return context


# дженерик для удаления товара
class ProductDelete(DeleteView):
    template_name = 'product_delete.html'
    # queryset = Product.objects.all()
    model = Product
    success_url = '/products/'


# Дженерик-заглушка для учебного шаблона 'product_list.html' (в проекте не используется)
# В отличие от дженериков, которые мы уже знаем, код здесь надо писать самому, переопределяя типы запросов
# (например get или post, вспоминаем реквесты из модуля C5)
class Products(View):

    def get(self, request):
        products = Product.objects.order_by('-price')
        # создаём объект класса пагинатор, передаём ему список наших товаров и их количество для одной страницы
        p = Paginator(products, 1)
        # берём номер страницы из get-запроса. Если ничего не передали, будем показывать первую страницу
        products = p.get_page(request.GET.get('page', 1))

        # теперь вместо всех объектов в списке товаров хранится только нужная нам страница с товарами
        data = {
            'products': products,
        }
        return render(request, 'product_list.html', data)
