# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product, Category  # Дополнительно импортируем категорию, чтобы пользователь мог её выбрать
from pprint import pprint
# from D7
from django.shortcuts import render
from django.views import View  # импортируем простую вьюшку
from django.core.paginator import Paginator  # импортируем класс, позволяющий удобно осуществлять постраничный вывод
from .filters import ProductFilter  # импортируем недавно написанный фильтр
from .forms import ProductForm  # импортируем нашу форму


# из списка на главной странице уберём всё лишнее
class ProductsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Product
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-price'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'products.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'products'
    paginate_by = 2  # поставим постраничный вывод в один элемент

    # Метод get_context_data позволяет нам изменить набор данных, который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами, что и были переданы.

        # В ответе мы должны получить словарь.
        # Забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса
        context = super().get_context_data(**kwargs)
        # Вписываем наш фильтр в контекст
        context['filter'] = ProductFilter(self.request.GET, queryset=self.get_queryset())
        try:
            context['parameter'] = context['filter'].data.urlencode()
        except AttributeError:
            pass
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.now()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_sale'] = None
        # context['next_sale'] = 'Wednesday Sale!'
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return ProductFilter(self.request.GET, queryset=queryset).qs


# дженерик для получения деталей о товаре
class ProductDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Product
    # Используем другой шаблон — product_detail.html
    template_name = 'product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# Дженерик для создания объекта.
# Надо указать только имя шаблона и класс формы. Остальное он сделает за вас
class ProductCreate(CreateView):
    template_name = 'product_create.html'
    form_class = ProductForm  # переносим форм класс, чтобы получать доступ к форме через метод POST

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# дженерик для редактирования объекта
class ProductUpdate(UpdateView):
    template_name = 'product_create.html'
    form_class = ProductForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся
    # редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Product.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# дженерик для удаления товара
class ProductDelete(DeleteView):
    template_name = 'product_delete.html'
    # queryset = Product.objects.all()
    model = Product
    success_url = '/products/'


# В отличие от дженериков, которые мы уже знаем, код здесь надо писать самому, переопределяя типы запросов (например
# гет или пост, вспоминаем реквесты из модуля C5)
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
