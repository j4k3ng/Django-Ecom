from django.db import transaction # I use this to avoid doing only one of the operation in save in case the light turn off
from rest_framework import serializers
from store.models import Product, Collection, Review, Customer, Cart, CartItem, Order, OrderItem
from decimal import Decimal
from pprint import pprint

# TO SERIALIZE THERE ARE 3 POSSIBILITIES:
# 1- IS TO CREATE A SERIALIZED MODEL COMPLETELY DISTINCT FROM THE ORIGINAL MODEL SO EVERYTHING FORM SCRATCH
# 2- IS TO TAKE THE ALREADY EXISTENT FIELD OF THE MODEL
# 3- THE BEST IS TO USE THE EXISTING MODEL BUT ADDING THE NEEDED FILEDS WHICH ARE NOT PRESENT IN THE MODEL

# METHOD 1
# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
#     price_with_tax = serializers.SerializerMethodField(
#         method_name='calculate_tax')
#     collection = serializers.PrimaryKeyRelatedField(
#         queryset=Collection.objects.all()
#     )
#     collection = serializers.StringRelatedField() #this works beccause the __str__ representation of colleciton is collection.name

#     def calculate_tax(self, product: Product):
#         return product.unit_price * Decimal(1.1)

# METHOD 3
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['pk', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True) #ready_only is used to avoid adding product_count while PUT
    # products_count = serializers.SerializerMethodField(
    #     method_name='count_collection', read_only=True)

    # def count_collection(self, collection: Collection):
    #     queryset = Product.objects.filter(collection= collection).count()
    #     return queryset

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['pk', 'title', 'description', 'slug', 'inventory',
                  'last_update', 'unit_price', 'price_with_tax', 'collection']

    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)

class ReviewSerializer(serializers.ModelSerializer):
    # customer = serializers.SerializerMethodField()
    class Meta:
        model = Review 
        fields = ['id', 'customer', 'description', 'date', 'stars']
        # depth = 1
    
    # def get_customer(self, obj):
    #     return obj.customer.first_name
    #customer_name= serializers.ReadOnlyField(source='customer.first_name')
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['customer'] = Customer.objects.filter(id=data['customer']).get().first_name
        return data

    def create(self, validated_data):   # instead of providing the product_id when creating a new review I can take it from the context which comes from the viewset 
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data) # when creating a new review the product_id is taken from the url and all the other data are taken form validated_data



class SimpleProductSerializer(serializers.ModelSerializer): # I create another serializer for Products with only title and unit_price to use it in the CartItemSerializer
    class Meta:
        model = Product
        fields = ['pk', 'title', 'unit_price']

class CartItemSerializer(serializers.ModelSerializer):  # The serializer used when getting cart 'GET' request on CartItem view
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = CartItem    
        fields = ['id', 'product', 'quantity', 'total_price']

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price


class CartSerializer(serializers.ModelSerializer):  # The serializer used when working with /carts
    id = serializers.UUIDField(read_only=True)  
    items = CartItemSerializer(many=True, read_only=True)
    total_cart = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart 
        fields = ['id', 'created_at', 'items', 'total_cart']

    def get_total_cart(self, cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])


class AddCartItemSerialier(serializers.ModelSerializer): # the serializer used when POST into CartItem view.
    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

    product_id = serializers.IntegerField()

    def validate_product_id(self, value): # used to avoid putting negative number in the product_id. Like add product_id = -1 which doesnt exist
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("No product with this id")
        return value

    def save(self, **kwargs):   # I need to overrite the save method to avoid getting the same product 2 times in the cart. In fact oppositely I need to add a quantity into existing product
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        try: # if the product is already in the cart just change the quantity and save
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist: # create a brand new product in the Cart if there is not
            self.instance = CartItem.objects.create(cart_id=cart_id, product_id=product_id, quantity=quantity)
        
        return self.instance

class UpdateCartItemSerialier(serializers.ModelSerializer): # serializer used when PATCH into the cartitem view. Basically i can only change the quantity
    class Meta:
        model = CartItem
        fields = ['quantity']

    
# I add a customer serializer here just to create a customer just after a new user is created
# NB: I cannot permit that the Customer data are fulfilled in the same call with the User data (email,fist_name,last_name) because those fields are fulfilled in the core app serializer and I cannot mixup the things.
# So basically the core serializer has the duty of just using the User data to login.
# So in the front end what we will do is that we will make 2 calls: the first one with just the User data to login and then the second one to fulfill the Customer data (birt_date ecc..). Everything will be in the same front end form but with 2 different API calls
class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer 
        fields = ['user_id', 'phone', 'birth_date', 'membership']


# Create a OrderItem serializer to put into OrderSerializer
class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer() 
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'unit_price']

# Create a Order Serializer
class OrderSerializer(serializers.ModelSerializer):  # The serializer used when working with /carts    
    orderitem_set = OrderItemSerializer(many=True)
    class Meta:
        model = Order 
        fields = ['id', 'placed_at', 'cart', 'orderitem_set']    

# Use this serializer when POST a new order because the other one include items which it's not needed to create a new order. We just need cart_id and user_id. Basically I only put cart_id because user_id is taken from the request by the jwt token
class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order 
        fields = ['cart']

    def validate_cart(self, cart):    # I define this method to avoid crating orders with empty cart or not existing cart_id
        if not Cart.objects.filter(id=cart.id).exists():    # I actually dont need this method because is already automatically check in some other validators
            raise serializers.ValidationError('No cart with this cart_id')
        if CartItem.objects.filter(cart=cart.id).count() == 0:
            raise serializers.ValidationError('You cannot create an empty cart')

    # I create a new order and pass the cart itmes in the order. Then I delete the cart. 
    def save(self):
        with transaction.atomic():
            user_id = self.context['user_id']
            cart_id = self.validated_data['cart'].id
            order = Order.objects.create(customer_id=user_id, cart_id=cart_id)  #creating the order with the customer_id and cart_id
            # Now I need to add all the products in the cart inside the OrderItem and then push the orderItems in the just created order
            cart_items = CartItem.objects.select_related('product').filter(cart_id=cart_id)  # create the queryset withh all the items in the given cart
            queryset = [    # here I create a list of all the orderitems
                OrderItem(
                    order=order,
                    product=item.product,
                    unit_price=item.product.unit_price,
                    quantity=item.quantity
                ) for item in cart_items
            ]
            OrderItem.objects.bulk_create(queryset) # Now i push all the queryset. So basically instead of doing OrderItem.objects.create() for all the items in the cart I just put everything in bulk in one time.

            Cart.objects.filter(id=cart_id).delete()    # after the order is created I delete the cart

            return order # I return the created order