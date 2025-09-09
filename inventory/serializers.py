from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, InventoryItem, Customer, Sale, InventoryLog
from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'quantity', 'price']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class InventoryItemSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(write_only=True, source='category', queryset=Category.objects.all(), required=False, allow_null=True)

    class Meta:
        model = InventoryItem
        fields = ['id','owner','name','dose','description','category','category_id','quantity','price','date_added','last_updated']

    def create(self, validated_data):
        # category is already in validated_data if provided
        request = self.context.get('request')
        validated_data['owner'] = request.user
        return super().create(validated_data)

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    sold_by = serializers.ReadOnlyField(source='sold_by.username')
    class Meta:
        model = Sale
        fields = ['id','item','customer','quantity','total_price','sold_by','date']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['sold_by'] = request.user
        # total_price could be passed or computed:
        if 'total_price' not in validated_data or validated_data['total_price'] in (None,):
            validated_data['total_price'] = validated_data['item'].price * validated_data['quantity']
        return super().create(validated_data)

class InventoryLogSerializer(serializers.ModelSerializer):
    changed_by = serializers.ReadOnlyField(source='changed_by.username')
    class Meta:
        model = InventoryLog
        fields = ['id','item','change_amount','change_type','timestamp','changed_by']
