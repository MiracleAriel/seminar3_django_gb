from django.shortcuts import render
from datetime import datetime, timedelta

def customer_orders(request, customer_id):
    # Получите клиента по customer_id
    customer = Customer.objects.get(id=customer_id)

    # Вычислите даты для фильтрации заказов
    end_date = datetime.now()
    start_date_week = end_date - timedelta(days=7)
    start_date_month = end_date - timedelta(days=30)
    start_date_year = end_date - timedelta(days=365)

    # Получите заказы клиента за разные периоды времени
    orders_week = Order.objects.filter(customer=customer, date_ordered__range=(start_date_week, end_date))
    orders_month = Order.objects.filter(customer=customer, date_ordered__range=(start_date_month, end_date))
    orders_year = Order.objects.filter(customer=customer, date_ordered__range=(start_date_year, end_date))

    # Соберите уникальные товары из заказов
    unique_products_week = set()
    for order in orders_week:
        unique_products_week.update(order.products.all())

    unique_products_month = set()
    for order in orders_month:
        unique_products_month.update(order.products.all())

    unique_products_year = set()
    for order in orders_year:
        unique_products_year.update(order.products.all())

    context = {
        'customer': customer,
        'unique_products_week': unique_products_week,
        'unique_products_month': unique_products_month,
        'unique_products_year': unique_products_year,
    }

    return render(request, 'customer_orders.html', context)

path('customer_orders/<int:customer_id>/', customer_orders, name='customer_orders')


from django.shortcuts import render, redirect
from .forms import ProductForm

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Replace 'product_list' with the URL for your product list page
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})
