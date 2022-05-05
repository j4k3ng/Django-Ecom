from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .models import Collection
from .models import Review
from .serializers import ProductSerializer
from .serializers import CollectionSerializer
from .serializers import ReviewSerializer
from rest_framework import status
from django.db.models import Count

from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
# Create your views here.

# THERE ARE 4 TYPES OF VIEWS:
# 1) FUNCTION BASED VIEWS -> easy and customizable
# 2) CLASS BASED VIEWS -> avoid ifs == 'GET' 
# 3) CLASS BASED VIEWS USING GENERIC VIEWS -> select the correct generic views and pass the queryset and serializer class
# 4) CLASS BASED VIEWS COMBINED IN VIEWSETS  -> combines different generic views together like list all products and single product detail

# GET AND POST PRODUCTS FUNCTION BASED VIEW
# @api_view(['GET', 'POST'])
# def product_list(request):
#     if request.method == 'GET':
#         queryset = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         print(serializer.validated_data)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# SAME VIEW BUT CLASS BASED AS ABOVE BUT CLASS BASED
# class ProductList(APIView):
#     def get(self, request):
#         queryset = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(queryset, many=True, context={'request':request})
#         return Response(serializer.data)

#     def post():
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         print(serializer.validated_data)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# SAME VIEW BUT USING A GENERIC VIEW
# class ProductList(ListCreateAPIView):
#     # queryset = Product.objects.select_related('collection').all() # easier way if you dont want to change things
#     # serializer_class = ProductSerializer

#     def get_queryset(self):
#         return Product.objects.select_related('collection').all()

#     def get_serializer_class(self):
#         return ProductSerializer

#     def get_serializer_context(self):
#         return {'request': self.request}


# GET, PUT, PATCH, DELETE A PRODUCT FUNCTION BASED VIEW
# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# def product_detail(request, id):
#     product = get_object_or_404(Product, pk=id)
#     if request.method == 'GET':
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     elif request.method == 'PATCH':
#         serializer = ProductSerializer(
#             product, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if product.orderitems.count() > 0:
#             return Response({'error': 'product cannot be deleted because it is associated with an order item'},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# SAME VIEW BUT CLASS BASED AS ABOVE BUT CLASS BASED
# class ProductDetail(APIView):
#     def get(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)

#     def patch(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(
#             product, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#     def put(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def delete(self, request, id):
#         if product.orderitems.count() > 0:
#             return Response({'error': 'product cannot be deleted because it is associated with an order item'},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# SAME VIEW BUT USING A GENERIC VIEW
# class ProductDetail(RetrieveUpdateDestroyAPIView):
# #     # queryset = Product.objects.select_related('collection').all() # easier way if you dont want to change things
# #     # serializer_class = ProductSerializer

#     def get_queryset(self):
#         return Product.objects.select_related('collection').all()

#     def get_serializer_class(self):
#         return ProductSerializer

#     def delete(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         if product.orderitems.count() > 0:
#             return Response({'error': 'product cannot be deleted because it is associated with an order item'},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

### NOW I COMBINE ProductList and ProductDetail usinga  ViewSet 
class ProductViewSet(ModelViewSet):
    def get_queryset(self):
        queryset = Product.objects.all()
        collection_id = self.request.query_params.get('collection_id')
        if collection_id is not None:
            queryset = queryset.filter(collection_id = collection_id)
        return queryset
        
    def get_serializer_class(self):
        return ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}   

    def destroy(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 0:
            return Response({'error': 'product cannot be deleted because it is associated with an order item'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
        

    # def delete(self, request, pk):
    #     product = get_object_or_404(Product, pk=pk)
    #     if product.orderitems.count() > 0:
    #         return Response({'error': 'product cannot be deleted because it is associated with an order item'},
    #                         status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

# GET AND POST COLLECTIONS FUNCTION BASED VIEW
# @api_view(['GET', 'POST'])
# def collection_list(request):
#     if request.method == 'GET':
#         queryset = Collection.objects.annotate(
#             products_count=Count('product')).all()
#         serializer = CollectionSerializer(queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         print(serializer.validated_data)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# SAME AS ABOVE BUT CLASS BASED GENERIC VIEW
# class CollectionList(ListCreateAPIView):
#     # queryset = Collection.objects.annotate(products_count=Count('product')).all() # easier way if you dont want to change things
#     # serializer_class = CollectionSerializer

#     def get_queryset(self):
#         return Collection.objects.annotate(products_count=Count('product')).all()

#     def get_serializer_class(self):
#         return CollectionSerializer

# GET PUT PATCH DELETE A COLLECTION USING FUNCTION BASED VIEW
# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# def collection_detail(request, value):
#     queryset = Collection.objects.annotate(
#         products_count=Count('product')).all()

#     if isinstance(value, int):
#         collection = get_object_or_404(queryset, pk=value)
#     elif isinstance(value, str):
#         collection = get_object_or_404(queryset, title=value)

#     if request.method == 'GET':
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)
#     elif request.method == 'PATCH':
#         serializer = CollectionSerializer(
#             collection, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = CollectionSerializer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if Product.objects.filter(collection=collection).count() > 0:
#             return Response({'error': 'collection cannot be deleted because it has associated products'},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# SAME AS ABOVE BUT CLASS BASED GENERIC VIEW
# class CollectionDetail(RetrieveUpdateDestroyAPIView):
# #   queryset =  Collection.objects.annotate(products_count=Count('product')).all() # easier way if you dont want to change things
# #   serializer_class = CollectionSerializer

#     def get_queryset(self):
#         return Collection.objects.annotate(products_count=Count('product')).all()

#     def get_serializer_class(self):
#         return CollectionSerializer

#     def delete(self, request, pk):
#         collection = get_object_or_404(queryset, pk=pk)
#         if Product.objects.filter(collection=collection).count() > 0:
#             return Response({'error': 'collection cannot be deleted because it has associated products'},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

### NOW I COMBINE CollectionList and CollectionDetail using a ViewSet 
class CollectionViewSet(ModelViewSet):
    # queryset = Collection.objects.annotate(products_count=Count('product')).all() # easier way if you dont want to change things
    # serializer_class = CollectionSerializer

    def get_queryset(self):
        return Collection.objects.annotate(products_count=Count('product')).all()

    def get_serializer_class(self):
        return CollectionSerializer
    
    def destroy(self, request, pk, *args, **kwargs):
        collection = get_object_or_404(queryset, pk=pk)
        if Product.objects.filter(collection=collection).count() > 0:
            return Response({'error': 'collection cannot be deleted because it has associated products'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)       
        return super().destroy(request, *args, **kwargs)

    # def delete(self, request, pk):
    #     collection = get_object_or_404(queryset, pk=pk)
    #     if Product.objects.filter(collection=collection).count() > 0:
    #         return Response({'error': 'collection cannot be deleted because it has associated products'},
    #                         status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     collection.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)



# USING GENERIC VIEW TO CREATE A REVIEW LIST
# class ReviewList(ListCreateAPIView):
# #   queryset =  Review.objects.all() # easier way if you dont want to change things
# #   serializer_class = ReviewSerializer

#     def get_queryset(self):
#         return Review.objects.all()

#     def get_serializer_class(self):
#         return ReviewSerializer 

# # USING GENERIC VIEW TO CREATE A REVIEW DETAIL PAGE
# class ReviewDetail(RetrieveUpdateDestroyAPIView):
# #   queryset =  Review.objects.all() # easier way if you dont want to change things
# #   serializer_class = ReviewSerializer

#     def get_queryset(self):
#         return Review.objects.all()

#     def get_serializer_class(self):
#         return ReviewSerializer 

### NOW I COMBINE ReviewList and ReviewDetail using a ViewSet 
class ReviewViewSet(ModelViewSet):
#   queryset =  Review.objects.all() # easier way if you dont want to change things
#   serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.select_related('customer').filter(product_id=self.kwargs['product_pk'])

    def get_serializer_class(self):
        return ReviewSerializer 

    def get_serializer_context(self):   # taking the product_id from the url and passing to the context in order to provide it to the serializer
        return {'product_id': self.kwargs['product_pk']}    # the product_id is hidden in the kwargs dictionary in the 'product_pk' name. This name is taken from the name of the lookup value in the nested url which is 'product' which became 'product_id'