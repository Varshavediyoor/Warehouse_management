from rest_framework import serializers
from .models import Product, ProductVariantValue, Zone, Rack, Shelf, Bin, Category, CategoryVariant

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = "__all__"


class RackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rack
        fields = "__all__"


class ShelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shelf
        fields = "__all__"


class BinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bin
        fields = "__all__"
        

from .models import Category, CategoryVariant


class CategoryVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryVariant
        fields = ["id", "name"]


class CategorySerializer(serializers.ModelSerializer):
    variants = CategoryVariantSerializer(many=True)

    class Meta:
        model = Category
        fields = ["id", "name", "description", "has_expiry", "variants"]

    # CREATE CATEGORY + VARIANTS
    def create(self, validated_data):
        variants_data = validated_data.pop("variants")

        if validated_data.get("has_expiry"):
            if not any(v["name"].lower() == "expiry" for v in variants_data):
                variants_data.append({"name": "Expiry"})

        category = Category.objects.create(**validated_data)

        for v in variants_data:
            CategoryVariant.objects.create(category=category, **v)

        return category


    # UPDATE CATEGORY + RESET VARIANTS
    def update(self, instance, validated_data):
        variants_data = validated_data.pop("variants")

        if validated_data.get("has_expiry"):
            if not any(v["name"].lower() == "expiry" for v in variants_data):
                variants_data.append({"name": "Expiry"})

        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.has_expiry = validated_data.get("has_expiry", instance.has_expiry)
        instance.save()

        instance.variants.all().delete()

        for v in variants_data:
            CategoryVariant.objects.create(category=instance, **v)

        return instance




class ProductVariantValueSerializer(serializers.ModelSerializer):
    variant_name = serializers.CharField(source="variant.name", read_only=True)

    class Meta:
        model = ProductVariantValue
        fields = ["variant", "variant_name", "value"]



class ProductSerializer(serializers.ModelSerializer):
    variant_values = ProductVariantValueSerializer(many=True)

    class Meta:
        model = Product
        fields = ["id", "name", "category", "expiry_date", "variant_values"]

    def create(self, validated_data):
        variants = validated_data.pop("variant_values")
        product = Product.objects.create(**validated_data)

        for v in variants:
            ProductVariantValue.objects.create(product=product, **v)

        return product


    def update(self, instance, validated_data):
        variants = validated_data.pop("variant_values")

        instance.name = validated_data.get("name", instance.name)
        instance.category = validated_data.get("category", instance.category)
        instance.expiry_date = validated_data.get("expiry_date", instance.expiry_date)
        instance.save()

        instance.variant_values.all().delete()
        for v in variants:
            ProductVariantValue.objects.create(product=instance, **v)

        return instance

