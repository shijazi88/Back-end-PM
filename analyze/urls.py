# from django.urls import path
# from .views import AnalyzeAPIView, prediction_result

# urlpatterns = [
#     # POST /api/analyze/       ← لرفع الصور + session_id
#     path("", AnalyzeAPIView.as_view(), name="analyze"),

#     # GET /api/analyze/prediction/?session_id=...
#     path("prediction/", prediction_result, name="prediction-result"),
# ]

# analyze/urls.py
# from django.urls import path
# from .views import AnalyzeAPIView, prediction_result, ping

# app_name = "analyze"

# urlpatterns = [
#     # POST /api/analyze/
#     path("", AnalyzeAPIView.as_view(), name="analyze"),

#     # GET /api/analyze/prediction/?session_id=...
#     path("prediction/", prediction_result, name="prediction-result"),

#     # DEBUG: GET /api/analyze/ping/  → للتأكد إن الراوت واصل
#     path("ping/", ping, name="ping"),
# ]

# analyze/urls.py
from django.urls import path
from .views import AnalyzeAPIView, prediction_result, ping

app_name = "analyze"

urlpatterns = [
    # ✅ /api/analyze/  (المسار المفضل)
    path("", AnalyzeAPIView.as_view(), name="analyze"),
    # ✅ /api/analyze/analyze/  (توافق للخلف)
    path("analyze/", AnalyzeAPIView.as_view()),

    # النتائج
    path("prediction/", prediction_result, name="prediction-result"),

    # تشيك سريع
    path("ping/", ping, name="ping"),
]
