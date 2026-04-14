from django.urls import path
from .views import ImageProcessingView

urlpatterns = [
    path('image/<str:action>/', ImageProcessingView.as_view(), name='image_processing'),
]
