from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .models import Collection
from .models import Review
from .models import Cart
from .models import CartItem
from .models import Customer
from .models import Order
from .serializers import ProductSerializer
from .serializers import CollectionSerializer
from .serializers import ReviewSerializer
from .serializers import CartSerializer
from .serializers import CartItemSerializer
from .serializers import AddCartItemSerialier
from .serializers import UpdateCartItemSerialier
from .serializers import CustomerSerializer
from .serializers import OrderSerializer
from .serializers import CreateOrderSerializer
from rest_framework import status
from django.db.models import Count

from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from .permissions import IsAdminOrReadOnly
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
    permission_classes = [IsAdminOrReadOnly]
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
    permission_classes = [IsAdminOrReadOnly]
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
class CartViewSet(ListModelMixin, # only is_staff can list all the carts
                 CreateModelMixin, # Create a cart just simply posting an empty object
                 RetrieveModelMixin, # I use retrive because I dont want to show all the carts when calling /carts. So using retreive I can get a specific cart /carts/UUID
                 DestroyModelMixin, # Destroy a cart from its UUID. /carts/UUID
                 GenericViewSet): # cannot use ModelViewSet because I cant provide the get function for this view, otherwise I will get back all the carts when calling /carts url
    def get_queryset(self):
        return Cart.objects.prefetch_related('items__product').all()

    def get_serializer_class(self):
        return CartSerializer 

    def list(self, request, *args, **kwargs):   # Only is_staff can list all carts, the others can only see their cart
        if bool(request.user and request.user.is_staff):
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response("user not authorized to list all carts", status=status.HTTP_401_UNAUTHORIZED)
     

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

# CREATING A VIEW TO FULFILL THE CUSTOMER DATA AFTER LOGIN
from rest_framework.decorators import action # I need to when defining a special custom action "me"
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
class CustomerViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet): # I avoided CreateModelMixin because in my case the Customer is automatically created when a new user is created so I dont need to add a new customer from scratch

    def get_queryset(self): 
        return Customer.objects.all()
    
    def get_serializer_class(self):
        return CustomerSerializer   
    
    # def get_permissions(self):
    #     if self.request.method == 'GET':    # allow all users to get a customer details but need autentication for modify a customer
    #         return [AllowAny()]
    #     else:
    #         return [IsAuthenticated()]

    def get_permissions(self):
        return [IsAdminUser()]

    # @action is used to define custom routes in this case customer/me 
    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        try:
            customer = Customer.objects.get(user_id=request.user.id)
        except:
            return Response("customer id not found, invalid token", status=status.HTTP_401_UNAUTHORIZED)
        if request.method=='GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()   
            return Response(serializer.data)        

# CREATING A VIEW TO CREATE OR GET THE ORDERS
class OrderViewSet(ModelViewSet):
    def get_queryset(self):
        return Order.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer   
        else:
            return OrderSerializer
    
    def get_serializer_context(self): 
        return {'user_id': self.request.user.id}   

    def get_permissions(self):  # I use this permission to avoid anonymous user to see the post button
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        else:
            return [IsAuthenticatedOrReadOnly()]

    def list(self, request, *args, **kwargs):   # Only is_staff can list all orders, the others can only see their order
        if bool(request.user and request.user.is_staff):
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        elif request.user.is_authenticated:
            queryset = Order.objects.filter(customer_id=request.user.id)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)   
        else:
            return Response("user not authenticated", status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, *args, **kwargs):
        customer_id = Order.objects.filter(id=kwargs['pk']).get().customer_id
        if request.user.id == customer_id or request.user.is_staff:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)   
        else:
            return Response("user not authorized to see this order", status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request, *args, **kwargs): # basically here I create the new order in serializer.save() using the CreateOrderSerializer. But then to show the order data to the frontend I reponde with the OrderSerializer which contains all the order information. If i return the CreateOrderSerializer I would get only the cart_id back after creating the order with POST
        # if request.user.is_authenticated or request.user.is_staff:    # I dont need this line because I already have IsAuthenticated or Readonly
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # order = serializer.save()
        # serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
