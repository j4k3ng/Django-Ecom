from rest_framework import serializers
from store.models import Product, Collection
from decimal import Decimal


# TO SERIALIZE THERE ARE 3 POSSIBILITIES:
# 1- IS TO CREATE A SERIALIZED MODEL COMPLETELY DISTINCT FROM THE ORIGINAL MODEL SO EVERYTHING FORM SCRATCH
# 2- IS TO TAKE THE ALREADY EXISTENT FIELD OF THE MODEL
# 3-THE BEST IS TO USE THE EXISTING MODEL BUT ADDING THE NEEDED FILEDS WHICH ARE NOT PRESENT IN THE MODEL

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
        fields = ['pk', 'title']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['pk', 'title', 'unit_price', 'price_with_tax', 'collection']

    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
