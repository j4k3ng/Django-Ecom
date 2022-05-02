from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from store.models import Product
from store.models import Customer
from store.models import Collection
from store.models import Order
from store.models import OrderItem


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

    # Example of getting all the orders made by a customer named "Mara"
    # customer_name = "Mara"
    # customer_id = Customer.objects.filter(first_name=customer_name).get().id
    # queryset = Order.objects.filter(customer_id=customer_id)

    # Example of getting the names of all the products tha have been ordered
    # product_id_filter = OrderItem.objects.values_list('product_id').distinct()
    # queryset = Product.objects.filter(
    #     id__in=product_id_filter).order_by('title')

    # Example of getting the last 5 orders and the associated customer and products for each order
    # queryset = Order.objects.select_related(
    #     'customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]

    # Example of inserting a new colleciton into the database NB:there is also a shorter way
    # collection = Collection()
    # collection.title = 'Video Games'
    # collection.featured_product = Product(pk=1)
    # collection.save()

    # Example of updating the title of a collection
    # collecton = Collection.objects.get(title='Video Games')
    # collection.title = 'Porn'
    # collection.save()

    # Example of deleting a collection
    # Collection.objects.filter(title='Video Games').delete()

    # Example of a transaction, use it when you want to run all of the block and
    # do not risk of creating an order without an order item if order items fails
    # with transaction.atomic():
    #     order = Order()
    #     order.customer_id = 1
    #     order.save()

    #     item = OrderItem()
    #     item.order = order
    #     item.product_id = 1
    #     item.quantity = 1
    #     item .unit_price = 10
    #     item.save()

    return render(request, 'hello.html', {'name': 'Mosh'})
