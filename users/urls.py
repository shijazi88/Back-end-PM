# users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RegisterView, UserLoginView
from .views import PasswordResetRequestView, PasswordResetConfirmView


router = DefaultRouter()
router.register("", UserViewSet, basename="user")  # بدل ما كانت 'users'

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("", include(router.urls)),
     path("password-reset/", PasswordResetRequestView.as_view(), name="password-reset"),
    path("password-reset-confirm/", PasswordResetConfirmView.as_view(), name="password-reset-confirm"),

]
