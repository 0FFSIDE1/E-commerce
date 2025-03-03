from django.urls import path
from .views import *
urlpatterns = [

    path('api/v1/coupon/create', AddCouponView.as_view(), name='create-coupon'),
    path('api/v1/coupon/<int:pk>/delete', DeleteCouponView, name='delete-coupon'),
    path('api/v1/coupon/apply-coupon', ApplyCouponView, name='apply-coupon'),


]
