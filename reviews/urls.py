from django.urls import path
from .views import *



urlpatterns = [
      path('api/v1/product/<str:pk>/review/create', CreateProductReview, name='product-review'),
      path('api/v1/product/<int:pk>/review', ProductReviewDetail, name='product-review-detail'),
      path('api/v1/order/<str:pk>/review/create', CreateOrderReview, name='order-review'),
      path('api/v1/order/<int:pk>/review', OrderReviewDetail, name='order-review-detail'),
      path('api/v1/vendor/<str:pk>/review/create', CreateVendorReview, name='vendor-review'),
      path('api/v1/vendor/<int:pk>/review', VendorReviewDetail, name='vendor-review-detail'),
      path('api/v1/vendor/reviews', GetAllReviewsForAVendor, name='all-vendor-reviews'),
      path('api/v1/product/reviews', GetAllReviewsForAProduct, name='all-product-reviews'),

]

