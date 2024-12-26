from django.urls import path
from .views import OTPVerificationView, UserRegisterView, LoginView, UserUpdateView, PasswordChangeView, SendOtpView, VerifyOtpView, ResendOTPView, UserDetailView, AdminUserView, SessionCheckView
# from django.views.generic import TemplateView
app_name = 'apps.users'
urlpatterns = [
    # User-related views
    path('register/', UserRegisterView.as_view(), name='register'),
    path('register-verify-otp/', OTPVerificationView.as_view(), name='verify-otp'),
    path('user/<int:user_id>/update/', UserUpdateView.as_view(), name='user-update'),
    path('change-password/', PasswordChangeView.as_view(), name='change-password'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
    
    # OTP-related views
    path('forget-password/', SendOtpView.as_view(), name='forget-password'),
    path('verify-otp/', VerifyOtpView.as_view(), name='verify-otp'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend-otp'),

    # Login and JWT authentication views
    path('login/', LoginView.as_view(), name='login'),  # Custom LoginView (if you have custom logic)
    path('api/session-check/', SessionCheckView.as_view(), name='session-check'),
    # Page rendering vie
    
    # admins crud should
    path('admin/users/', AdminUserView.as_view(), name='admin-users-list'),  # For listing users
    path('admin/users/<int:user_id>/', AdminUserView.as_view(), name='admin-user-detail'),  # For updating, deleting, or changing password for a user
    # path('admin/users/<int:user_id>/change-password/', ChangePasswordView.as_view(), name='change-password'),
]