from rest_framework import serializers
from sellers.models import Vendor

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ["name","address", "email", "phone", "currency"]

    # def validate(self, data):
    #     request = self.context.get('request')
    #     user = request.user
    #     if user.is_anonymous:
    #         raise serializers.ValidationError("Anonymous users cannot access this data.")
    #     return data