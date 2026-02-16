from .auth import RegisterView, LoginView
from .otp import VerifyOTPView, ResendOTPView
from .telegram import TelegramLinkConfirmView
from .me import MeView
from .selfie import UploadSelfieView
from .password_reset import ForgotPasswordView, ConfirmResetView, ResetPasswordView
from .locations import RegionListView, DistrictListView
from .profile import ProfileCompleteView
from .photos import UserPhotoListCreateView, UserPhotoDeleteView, UserPhotoSetMainView  