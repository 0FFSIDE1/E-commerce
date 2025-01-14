from rest_framework import serializers
from sellers.models import Vendor, User

class SellerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = Vendor
        fields = ["full_name", "brand_name", "address", "email", "phone", "currency", 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        errors = []
        if not data.get('full_name'):
            errors.append({'field': 'firstName', 'message': 'This field is required'})
        if not data.get('brand_name'):
            errors.append({'field': 'lastName', 'message': 'This field is required'})
        if not data.get('email'):
            errors.append({'field': 'email', 'message': 'This field is required'})
        if not data.get('password'):
            errors.append({'field': 'password', 'message': 'This field is required'})
        if User.objects.filter(email=data.get('email')).exists():
            errors.append({'field': 'email', 'message': 'Email already exists'})
        if errors:
            raise serializers.ValidationError({'errors': errors})
        return data
    

