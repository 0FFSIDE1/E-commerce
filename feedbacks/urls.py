from django.urls import path
from .views import *



urlpatterns = [
   path('api/v1/feedback/create', CreateFeedback, name='create-feedbacks'),
   path('api/v1/feedback', GetFeedback, name='all-feedbacks'),
   path('api/v1/<int:pk>/feedback', GetFeedbackDetail, name='feedback-detail'),
    
]
