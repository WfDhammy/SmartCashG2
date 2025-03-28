from django.urls import path
from .google import GoogleAuthView
from . import views

urlpatterns = [
    path('google', GoogleAuthView.as_view(), name="Google Authentication"),
    path('signup/', views.UserSignup.as_view(), name="Signup"),
    path('login', views.LoginView.as_view(), name="Login"),
    path('', views.UserProfileView.as_view(), name="all users"),
    # path('otp-request/', views.otp_request, name='otp_request'),
]