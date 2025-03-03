from rest_framework import serializers
from reviews.models import *

class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = '__all__'


class OrderReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderReview
        fields = '__all__'

class VendorReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorReview
        fields = '__all__'