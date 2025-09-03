# users/serializers.py
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import get_user_model

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = CustomUser
        fields = ["id", "email", "password", "full_name", "role"]
        extra_kwargs = {"password": {"write_only": True}, "role": {"read_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        # 🟢 أي يوزر جديد بياخد role=user
        user = CustomUser(**validated_data)
        user.role = "user"
        user.set_password(password)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "full_name", "role", "is_active"]

User = get_user_model()

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        # ما نرجّعش خطأ لو الإيميل مش موجود (منع enumeration)
        self.user = User.objects.filter(email__iexact=value).first()
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8, write_only=True)

    def validate(self, attrs):
        from django.utils.http import urlsafe_base64_decode
        from django.contrib.auth.tokens import PasswordResetTokenGenerator

        uidb64 = attrs.get("uidb64")
        token = attrs.get("token")
        new_password = attrs.get("new_password")

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
        except Exception:
            raise serializers.ValidationError({"uidb64": "Invalid UID"})

        User = get_user_model()
        try:
            user = User.objects.get(pk=uid, is_active=True)
        except User.DoesNotExist:
            raise serializers.ValidationError({"uidb64": "Invalid user"})

        token_gen = PasswordResetTokenGenerator()
        if not token_gen.check_token(user, token):
            raise serializers.ValidationError({"token": "Invalid or expired token"})

        # اختياري: سياسات كلمة السر (تأكيد تعقيدها أو استخدام validators)
        self.user = user
        self.new_password = new_password
        return attrs

    def save(self):
        self.user.set_password(self.new_password)
        self.user.save()
        return self.user

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        self.user = User.objects.filter(email__iexact=value).first()
        return value

class PasswordResetConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8, write_only=True)

    def validate(self, attrs):
        from django.utils.http import urlsafe_base64_decode
        from django.contrib.auth.tokens import PasswordResetTokenGenerator

        uidb64 = attrs["uidb64"]
        token = attrs["token"]
        new_password = attrs["new_password"]

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
        except Exception:
            raise serializers.ValidationError({"uidb64": "Invalid UID"})

        try:
            user = User.objects.get(pk=uid, is_active=True)
        except User.DoesNotExist:
            raise serializers.ValidationError({"uidb64": "Invalid user"})

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError({"token": "Invalid or expired token"})

        self.user = user
        self.new_password = new_password
        return attrs

    def save(self):
        self.user.set_password(self.new_password)
        self.user.save()
        return self.user
