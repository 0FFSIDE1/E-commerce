from rest_framework import serializers
from sellers.models import Vendor, User, Category, Store
from django.contrib.auth.password_validation import validate_password

class SellerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = Vendor
        fields = [
            "first_name", "last_name", "brand_name", "address", "email", "phone", "currency", 'password', "city", "country", "state", "category", "brand_type", "username", 
            ]
        extra_kwargs = {
            'password': {
                'write_only': True,
                },
        }

    def validate_category(self, value):
        """
        Validate that the provided category matches one of the choices in the Category model.
        """
        # Check if the value exists in the keys of the TextChoices enumeration
        if value not in Category.values:
            raise serializers.ValidationError(
                f"Invalid category '{value}'. Valid options are: {', '.join(Category.values)}."
            )
        return value

    def validate_brand_type(self, value):
        """
        Validate that the provided brand_type matches one of the choices in the Store model.
        """
        if value not in Store.values:
            raise serializers.ValidationError(
                f"Invalid brand type '{value}'. Valid options are: {', '.join(Store.values)}."
            )
        return value

    def validate(self, data):
        errors = []
        # Required fields and their error messages
        required_fields = {
            'username': 'This field is required',
            'first_name': 'This field is required',
            'last_name': 'This field is required',
            'brand_name': 'This field is required',
            'email': 'This field is required',
            'address': 'This field is required',
            'password': 'This field is required',
            'city': 'This field is required',
            'state': 'This field is required',
            'country': 'This field is required',
            'category': 'This field is required',
            'brand_type': 'This field is required',
        }
        
        # Check for missing required fields
        for field, message in required_fields.items():
            if not data.get(field):
                errors.append({'field': field, 'message': message})
        
        # Check for unique email
        if 'email' in data and User.objects.filter(email=data.get('email')).exists():
            errors.append({
                'field': 'email',
                'message': 'Vendor with this email already exists'
            })

        # Use Django's built-in password validation
        password = data.get('password')
        if password:
            
            try:
                validate_password(password)
            except serializers.ValidationError as password_errors:
                errors.extend([{'field': 'password', 'message': msg} for msg in password_errors.messages])

        
        # Raise validation error if any issues found
        if errors:
            raise serializers.ValidationError(errors)
        
        return data
    

class LoginVendorSerializer(serializers.Serializer):
    username = serializers.CharField()
   
    password = serializers.CharField()



class UpdateVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

    def update(self, instance, validated_data):
        """
        Perform the update on the Vendor instance.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
