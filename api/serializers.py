from rest_framework import serializers

from .models import Categorymodel,Productmodel,Cartmodel,Ordermodel,User

class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model=User

        fields=['id','username','first_name','last_name','email','password']

        read_only_fields=['id']

    def create(self, validated_data):
        
        return User.objects.create_user(**validated_data)

class ProductSerializer(serializers.ModelSerializer):

    product_category=serializers.StringRelatedField(read_only=True)

    class Meta:

        model=Productmodel

        fields="__all__"

        read_only_fields=["id","product_category"]

class CategorySerializer(serializers.ModelSerializer):

    products=ProductSerializer(many=True,read_only=True)

    class Meta:

        model=Categorymodel

        fields="__all__"

        read_only_fields=["id"]

class CartSerializer(serializers.ModelSerializer):

    cart_product=serializers.StringRelatedField(read_only=True)

    cart_user=serializers.StringRelatedField(read_only=True)

    class Meta:

        model=Cartmodel

        fields="__all__"

        read_only_fields=['cart_product','cart_user','cart_date','id']

class OrderSerializer(serializers.ModelSerializer):

    order_product=serializers.StringRelatedField(read_only=True)

    order_user=serializers.StringRelatedField(read_only=True)

    class Meta:

        model=Ordermodel

        fields="__all__"

        read_only_fields=['order_product','order_user','order_date','id']

    
