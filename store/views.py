from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .models import Collection
from .models import Review
from .models import Cart
from .models import CartItem
from .serializers import ProductSerializer
from .serializers import CollectionSerializer
from .serializers import ReviewSerializer
from .serializers import CartSerializer
from .serializers import CartItemSerializer
from .serializers import AddCartItemSerialier
from .serializers import UpdateCartItemSerialier
from rest_framework import status
from django.db.models import Count

from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
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

    def get_queryset(self): # this method is used to query the product url with a collection_id in order to show all the products in that collection
        queryset = Product.objects.all()
        collection_id = self.request.query_params.get('collection_id') # the collection is taken from the query_params dictionary in the request object. I use get() instead of [] just because if you dont provide a collection_id query you will get an error using [] instead get return none
        if collection_id is not None:  # if a query with collection_id is provided filter all the product based on the queryset otherwise return all the products
            queryset = queryset.filter(collection_id = collection_id)
        else:
            return queryset
        
    def get_serializer_class(self):
        return ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}   

    def destroy(self, request, pk, *args, **kwargs): # I use destroy instead of delete because otherwise the delete button will appear also in the product list instead of only on the proudct detail page
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
    
    def destroy(self, request, pk, *args, **kwargs):# I use destroy instead of delete because otherwise the delete button will appear also in the collection list instead of only on the collection detail page
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
        return Review.objects.select_related('customer').filter(product_id=self.kwargs['product_pk']) # I need to specify the product_id when taking the reviews from a product otherwise all the reviews of all products will be shown for each product review page

    def get_serializer_class(self):
        return ReviewSerializer 

    def get_serializer_context(self):   # taking the product_id from the url and passing to the context in order to provide it to the serializer
        return {'product_id': self.kwargs['product_pk']}    # the product_id is hidden in the kwargs dictionary in the 'product_pk' name. This name is taken from the name of the lookup value in the nested url which is 'product' which became 'product_id'


## CREATING CART VIEW 
class CartViewSet(CreateModelMixin, # Create a cart just simply posting an empty object
                 RetrieveModelMixin, # I use retrive because I dont want to show all the carts when calling /carts. So using retreive I can get a specific cart /carts/UUID
                 DestroyModelMixin, # Destroy a cart from its UUID. /carts/UUID
                 GenericViewSet): # cannot use ModelViewSet because I cant provide the get function for this view, otherwise I will get back all the carts when calling /carts url
    def get_queryset(self):
        return Cart.objects.prefetch_related('items__product').all()

    def get_serializer_class(self):
        return CartSerializer 

## CREATING A ITEM VIEW INSIDE CART URL TO MODIFY AND SEE IN DETAILS THE ITEMS IN THE CART /carts/items/(item number in the cart)
class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    def get_queryset(self):
        return CartItem.objects.select_related('product').filter(cart_id=self.kwargs['cart_pk'])

    def get_serializer_class(self): # I use different serializer based on the what I need to do in the page
        if self.request.method == "GET":
            return CartItemSerializer 
        elif self.request.method == "PATCH":
            return UpdateCartItemSerialier
        elif self.request.method == "POST":
            return AddCartItemSerialier
            
    def get_serializer_context(self): 
        return {'cart_id': self.kwargs['cart_pk']}   
