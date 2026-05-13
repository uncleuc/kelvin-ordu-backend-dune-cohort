from rest_framework import serializers
from .models import Product, Category
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'

    def get_product_count(self, obj):
        return obj.products.count()


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock', 'image', 'category', 'category_id', 'is_available', 'created_at', 'created_by']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Only allow creator to update
        if instance.created_by != self.context['request'].user:
            raise serializers.ValidationError("You can only edit your own products.")
        return super().update(instance, validated_data)
