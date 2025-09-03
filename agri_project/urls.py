# # agri_project/urls.py
# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("api/users/", include("users.urls")),
#     path('api/', include('users.urls')),
#     path("api/analyze/", include("analyze.urls")),
#     path("api/payments/", include("payments.urls")), # 👈 مهم
# ]

# # لخدمة ملفات الميديا في التطوير
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# agri_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/analyze/", include("analyze.urls", namespace="analyze")),
    path("api/users/", include("users.urls")),
    path("api/payments/", include("payments.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
