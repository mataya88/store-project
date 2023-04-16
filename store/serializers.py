from decimal import Decimal
from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        models = Category
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'category']
        # fields = '__all__'
    
    """
    def create(self, validated_data):
        # to edit the prot mechanism
        product = Product(**validated_data)
        product.inventory = 100
        product.save()
        return product
    """

    # def update(self, instance, validated_data):
    #     instance.unit_price = validated_data.get('unit_price') + 20
    #     instance.save()
    #     return instance
    # category = serializer.StringRelatedField() uses str func
    # category = CategorySerializer() to get the object
    #category = serializers.HyperLinkedRelatedField(
    #    queryset=Category.objects.all(),
    #    view_name='category-detail'
    #)
    price = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        source='unit_price'
    )

    