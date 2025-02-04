from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Order
from .forms import OrderForm, OrderSearchForm


def create_order(request: HttpRequest) -> HttpResponse:
    """
    Создает новый заказ и сохраняет его в базе данных.

    Если метод запроса POST, обрабатывает форму создания заказа и сохраняет данные.
    В случае успешного создания перенаправляет на список заказов.
    Если метод GET, отображает пустую форму.

    :param request: HTTP-запрос от клиента
    :return: HTTP-ответ с рендерингом страницы формы создания заказа
    """
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_list')
        else:
            print("Ошибки формы:", form.errors)
    else:
        form = OrderForm()

    return render(request, 'orders/create_order.html', {'form': form})


def delete_order(request: HttpRequest, order_id: int) -> HttpResponse:
    """
    Удаляет заказ по его идентификатору.

    :param request: HTTP-запрос от клиента
    :param order_id: Идентификатор удаляемого заказа
    :return: Перенаправление на страницу списка заказов
    """
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('order_list')


def update_order_status(request: HttpRequest, order_id: int) -> HttpResponse:
    """
    Обновляет статус заказа, если передано допустимое значение.

    :param request: HTTP-запрос от клиента (POST с параметром 'status')
    :param order_id: Идентификатор заказа
    :return: Перенаправление на список заказов после обновления статуса
    """
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Order.STATUS_CHOICES):
            order.status = status
            order.save()
        return redirect('order_list')

    return render(request, 'orders/update_order_status.html', {'order': order})


def search_orders(request: HttpRequest) -> HttpResponse:
    """
    Выполняет поиск заказов по номеру стола или статусу.

    :param request: HTTP-запрос с параметром 'query' (поисковый запрос)
    :return: HTTP-ответ с рендерингом страницы списка заказов, соответствующих поиску
    """
    query = request.GET.get('query')

    if query:
        orders = Order.objects.filter(Q(table_number__icontains=query) | Q(status__icontains=query))
    else:
        orders = Order.objects.all()

    return render(request, 'orders/search_orders.html', {'orders': orders})


def order_list(request: HttpRequest) -> HttpResponse:
    """
    Отображает список заказов, позволяя фильтровать их по номеру стола и статусу.

    :param request: HTTP-запрос с возможными GET-параметрами фильтрации
    :return: HTTP-ответ с рендерингом страницы списка заказов
    """
    orders = Order.objects.all()
    form = OrderSearchForm(request.GET)

    if form.is_valid():
        table_number = form.cleaned_data.get('table_number')
        status = form.cleaned_data.get('status')

        if table_number:
            orders = orders.filter(table_number=table_number)
        if status:
            orders = orders.filter(status=status)

    return render(request, 'orders/order_list.html', {'orders': orders, 'form': form})


def calculate_revenue(request: HttpRequest) -> HttpResponse:
    """
    Рассчитывает общую сумму выручки от всех оплаченных заказов.

    :param request: HTTP-запрос от клиента
    :return: HTTP-ответ с рендерингом страницы, отображающей сумму выручки
    """
    revenue = Order.get_paid_revenue()
    return render(request, 'orders/calculate_revenue.html', {'revenue': revenue})


def edit_order(request: HttpRequest, order_id: int) -> HttpResponse:
    """
    Позволяет редактировать заказ по его идентификатору.

    Если метод запроса POST, обновляет данные заказа.
    Если метод GET, отображает форму редактирования.

    :param request: HTTP-запрос от клиента
    :param order_id: Идентификатор редактируемого заказа
    :return: HTTP-ответ с рендерингом страницы редактирования заказа
    """
    order = get_object_or_404(Order, pk=order_id)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)

    return render(request, 'orders/edit_order.html', {'form': form, 'order': order})
