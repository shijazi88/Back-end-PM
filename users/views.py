# users/views.py
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import UserRegisterSerializer
from .models import CustomUser
from rest_framework import viewsets, permissions
from .models import CustomUser
from .serializers import UserRegisterSerializer
from .serializers import UserSerializer

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerializer

#     def get_permissions(self):
#         if self.action in ["list", "retrieve", "update", "partial_update", "destroy"]:
#             return [permissions.IsAdminUser()]  # 👈 بس الأدمن يقدر يدير
#         return [permissions.IsAuthenticated()]   # 👈 أي يوزر مسجل دخول يقدر يشوف نفسه مثلاً

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  # لازم يكون معاه توكن



class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .auth_serializers import UserLoginSerializer

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer

User = get_user_model()

class PasswordResetRequestView(APIView):
    permission_classes = []  # allow any

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = getattr(serializer, "user", None)
        # نرجّع نفس الرد حتى لو مفيش يوزر (أمان)
        if user:
            token = PasswordResetTokenGenerator().make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

            # رابط الواجهة الأمامية (عدليه حسب الدومين)
            reset_link = f"{getattr(settings, 'FRONTEND_ORIGIN', 'http://localhost:3000')}/reset-password?uid={uidb64}&token={token}"

            subject = "Reset your password"
            message = (
                f"Hello,\n\nWe received a request to reset your password.\n"
                f"Open this link to set a new password:\n{reset_link}\n\n"
                f"If you did not request this, you can ignore this email."
            )
            send_mail(subject, message, getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@example.com"), [user.email], fail_silently=True)

        return Response({"detail": "If the email exists, you'll receive a reset link shortly."}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    permission_classes = []  # allow any

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)
    


from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer

User = get_user_model()

class PasswordResetRequestView(APIView):
    permission_classes = []  # AllowAny

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = getattr(serializer, "user", None)

        # نفس الرد سواء الإيميل موجود أو لا لمنع enumeration
        if user:
            token = PasswordResetTokenGenerator().make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"{getattr(settings, 'FRONTEND_ORIGIN', 'http://localhost:3000')}/reset-password?uid={uidb64}&token={token}"

            subject = "Reset your password"
            message = (
                "Hello,\n\nWe received a request to reset your password.\n"
                f"Open this link to set a new password:\n{reset_link}\n\n"
                "If you did not request this, you can ignore this email."
            )
            # أثناء التطوير خليه False عشان تشوفي الخطأ لو حصل
            send_mail(subject, message, getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@example.com"),
                      [user.email], fail_silently=False)

        return Response({"detail": "If the email exists, you'll receive a reset link shortly."}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    permission_classes = []  # AllowAny

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)
