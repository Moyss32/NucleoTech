from django.urls import path
from apps.users.views import RegisterView, ProfileView
from apps.subscriptions.views import DashboardView, SubscriptionDetailView
from apps.processing.views import HistoryListView, ProcessFileView, ProcessStatusView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Auth
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User
    path('user/profile/', ProfileView.as_view(), name='user_profile'),
    path('user/dashboard/', DashboardView.as_view(), name='user_dashboard'),
    
    # Subscription
    path('subscription/', SubscriptionDetailView.as_view(), name='subscription_detail'),
    
    # History
    path('history/', HistoryListView.as_view(), name='history_list'),
    
    # Processing
    path('process/', ProcessFileView.as_view(), name='process_file'),
    path('process/status/<str:task_id>/', ProcessStatusView.as_view(), name='process_status'),
]
