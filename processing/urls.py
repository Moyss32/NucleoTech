from django.urls import path
from .views import ImageProcessingView, AudioProcessingView

urlpatterns = [
    path('image/<str:action>/', ImageProcessingView.as_view(), name='image_processing'),
    path('audio/<str:action>/', AudioProcessingView.as_view(), name='audio_processing'),
]
