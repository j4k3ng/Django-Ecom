from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .models import Collection
from .serializers import ProductSerializer
from .serializers import CollectionSerializer
from rest_framework import status
# Create your views here.


@api_view()
def product_list(request):
    queryset = Product.objects.select_related('collection').all()
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view()
def product_detail(request, id):
    # product = Product.objects.get(pk=id)
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view()
def collection_list(request):
    queryset = Collection.objects.all()
    serializer = CollectionSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view()
def collection_detail(request, value):
    if isinstance(value, int):
        collection = get_object_or_404(Collection, pk=value)
    elif isinstance(value, str):
        collection = get_object_or_404(Collection, title=value)    
    serializer = CollectionSerializer(collection)
    return Response(serializer.data)
