"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, re_path
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="ALABALINE API DOC",
        default_version="v1",
        description="API documentation for the alabaline",
        # terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="info@offsideint.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],  # Anyone can view the docs
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('customers.urls')),
    path('', include('products.urls')),
    path('', include('sellers.urls')),
    path('', include('carts.urls')),
    path('', include('orders.urls')),
    path('', include('billings.urls')),
    path('', include('reviews.urls')),
    path('', include('feedbacks.urls')),
    path('', include('notifications.urls')),
    path('', include('newsletter.urls')),
    path('', include('app.urls')),
    path('', include('coupons.urls')),
    path('', include('wishlist.urls')),
    path('', include('waitlist.urls')),

    # Swagger & ReDoc URLs
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc-ui"),
]
