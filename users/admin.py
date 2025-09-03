# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
admin.site.site_header = "GIS Innovation Hub Admin"
admin.site.site_title = "GIS Admin Portal"
admin.site.index_title = "Welcome to GIS Innovation Hub Dashboard"


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "full_name", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("email", "full_name")
    ordering = ("email",)

    # نخلي الفورم بتاع الإضافة/التعديل يظهر فيه role
    fieldsets = (
        (None, {"fields": ("email", "password", "full_name", "role")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "full_name", "password1", "password2", "role", "is_staff", "is_active")}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)
#وح على /admin

# هتلاقي جدول اسمه Custom users

# اضغط Add

# اكتب:

# Email

# Full name

# Password

# Role = admin

# علم على is_staff + is_active

# وبكده بيبقى عندك أدمن رسمي.