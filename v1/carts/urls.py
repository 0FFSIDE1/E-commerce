from django.urls import path
from .views import (
    Create_View,
    Items_View,
    Update_View,
    Destroy_View,
   #  listview
)

urlpatterns = [
    path('', Create_View.as_view()),
    path("item/<str:customer_name>/", Items_View.as_view()),
    path("update/<int:pk>/", Update_View.as_view()),
    path("delete/<int:pk>/", Destroy_View.as_view())
   #   path("list/<str:customer_name>/", listview.as_view())
]
