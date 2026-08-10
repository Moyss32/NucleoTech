from django.urls import path
from apps.users.views import RegisterView, ProfileView
from apps.subscriptions.views import (
    DashboardView, SubscriptionDetailView, SubscriptionListView, PaymentHistoryView
)
from apps.subscriptions.stripe_views import (
    StripeCheckoutView, StripeBillingPortalView, stripe_webhook
)
from apps.processing.views import HistoryListView, ProcessFileView, ProcessStatusView
from apps.processing.download_views import SecureDownloadView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # -------------------------------------------------------------------------
    # Auth
    # -------------------------------------------------------------------------
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # -------------------------------------------------------------------------
    # User
    # -------------------------------------------------------------------------
    path('user/profile/', ProfileView.as_view(), name='user_profile'),
    path('user/dashboard/', DashboardView.as_view(), name='user_dashboard'),

    # -------------------------------------------------------------------------
    # Subscriptions
    # -------------------------------------------------------------------------
    path('subscriptions/', SubscriptionListView.as_view(), name='subscription_list'),
    path('subscription/', SubscriptionDetailView.as_view(), name='subscription_detail'),
    path('subscriptions/checkout/', StripeCheckoutView.as_view(), name='stripe_checkout'),
    path('subscriptions/portal/', StripeBillingPortalView.as_view(), name='stripe_portal'),
    path('subscriptions/webhook/', stripe_webhook, name='stripe_webhook'),
    path('subscriptions/payments/', PaymentHistoryView.as_view(), name='payment_history'),

    # -------------------------------------------------------------------------
    # Processing
    # -------------------------------------------------------------------------
    path('process/', ProcessFileView.as_view(), name='process_file'),
    path('process/status/<str:task_id>/', ProcessStatusView.as_view(), name='process_status'),
    path('process/remove-bg/', ProcessFileView.as_view(), name='process_remove_bg'),
    path('process/upscale/', ProcessFileView.as_view(), name='process_upscale'),
    path('process/convert-image/', ProcessFileView.as_view(), name='process_convert_image'),
    path('process/convert-audio/', ProcessFileView.as_view(), name='process_convert_audio'),
    path('process/thumbnail/', ProcessFileView.as_view(), name='process_thumbnail'),

    # -------------------------------------------------------------------------
    # History
    # -------------------------------------------------------------------------
    path('history/', HistoryListView.as_view(), name='history_list'),

    # -------------------------------------------------------------------------
    # Files
    # -------------------------------------------------------------------------
    path('files/<uuid:file_id>/download/', SecureDownloadView.as_view(), name='secure_download'),
]
