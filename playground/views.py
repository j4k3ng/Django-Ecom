from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product
from store.models import Customer
from store.models import Collection
from store.models import Order


def say_hello(request):
    # First query example
    #query_set = Product.objects.all()

    # Example of using try catch
    # try:
    #     product = Product.objects.get(pk=1)
    # except ObjectDoesNotExist:
    #     print("not Exist")

    # Example of filtering a product with unit_price > 20 usd
    # queryset = Product.objects.filter(unit_price__gt=20)
    # queryset = Customer.objects.filter(email__endswith="com")
    # queryset = Collection.objects.filter(featured_product_id__isnull=True)

    customer_name = "Mara"
    customer_id = Customer.objects.filter(first_name=customer_name).get().id
    queryset = Order.objects.filter(customer_id=customer_id)
    return render(request, 'hello.html', {'name': 'Mosh', 'orders': list(queryset), 'customer_name': customer_name, 'customer_id': customer_id})
