from rest_framework import serializers
from app.models import SubscriptionPlan, Subscription

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ['id', 'name', 'description', 'price', 'duration_in_days']



class SubscriptionSerializer(serializers.ModelSerializer):
    plan_details = SubscriptionPlanSerializer(source='plan', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)  # Fetch the full name of the user
    plan_name = serializers.CharField(source='plan.name', read_only=True)          # Fetch the name of the plan


    class Meta:
        model = Subscription
        fields = ['user', 'plan', 'user_name', 'plan_name', 'plan_details', 'start_date', 'expire_date', 'is_active', 'remaining_days']
        read_only_fields = ['start_date', 'expire_date', 'is_active', 'remaining_days']

    def validate(self, data):
        # Ensure only one active subscription per user
        if Subscription.objects.filter(user=self.context['request'].user, is_active=True).exists():
            raise serializers.ValidationError("User already has an active subscription.")
        return data