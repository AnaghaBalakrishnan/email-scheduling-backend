# users/urls.py
from django.urls import path
from .views import RegisterView, VerifyOTPView, ProfilePictureUpdateView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('profile/update/', ProfilePictureUpdateView.as_view(), name='update-profile'),

    # ADD THIS NEW URL PATTERN
    path('logout/', LogoutView.as_view(), name='logout'),
]