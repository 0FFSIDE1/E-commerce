from rest_framework import serializers
from waitlist.models import Waitlist

class WaitlistVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waitlist
        fields = ['email']

    def create(self, validated_data):
        """Handle unique constraint for email"""
        if Waitlist.objects.filter(email=validated_data["email"]).exists():
            raise serializers.ValidationError({"email": "This email is already registered."})
        return super().create(validated_data)