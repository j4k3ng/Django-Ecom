from rest_framework import serializers
from store.models import Product, Collection, Review, Customer
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
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['customer'] = Customer.objects.filter(id=data['customer']).get().first_name
        return data

    def create(self, validated_data):   # instead of providing the product_id when creating a new review I can take it from the context which comes from the viewset 
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data) # when creating a new review the product_id is taken from the url and all the other data are taken form validated_data

    # def get_customer(self, obj):
    #     return obj.customer.first_name
    #customer_name= serializers.ReadOnlyField(source='customer.first_name')