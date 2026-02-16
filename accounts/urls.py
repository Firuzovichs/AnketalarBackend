from django.urls import path
from accounts.views import (
    RegisterView, LoginView,
    VerifyOTPView, ResendOTPView,
    UploadSelfieView, MeView,
    TelegramLinkConfirmView,
    ForgotPasswordView, ConfirmResetView, ResetPasswordView,
    ProfileCompleteView,
    UserPhotoListCreateView, UserPhotoDeleteView, UserPhotoSetMainView,
)

urlpatterns = [
    path("me/profile/", ProfileCompleteView.as_view()),
    path("me/profile/", ProfileCompleteView.as_view()),

    path("photos/", UserPhotoListCreateView.as_view()),
    path("photos/<int:pk>/", UserPhotoDeleteView.as_view()),
    path("photos/<int:pk>/main/", UserPhotoSetMainView.as_view()),
    path("photos/", UserPhotoListCreateView.as_view()),
    path("photos/<int:pk>/", UserPhotoDeleteView.as_view()),
    path("photos/<int:pk>/main/", UserPhotoSetMainView.as_view()),
    path("register/", RegisterView.as_view()),
    path("verify-otp/", VerifyOTPView.as_view()),
    path("resend-otp/", ResendOTPView.as_view()),
    path("login/", LoginView.as_view()),
    path("me/", MeView.as_view()),
    path("upload-selfie/", UploadSelfieView.as_view()),
    path("telegram/confirm/", TelegramLinkConfirmView.as_view()),
    path("password/forgot/", ForgotPasswordView.as_view()),
    path("password/confirm/", ConfirmResetView.as_view()),
    path("password/reset/", ResetPasswordView.as_view()),
]
