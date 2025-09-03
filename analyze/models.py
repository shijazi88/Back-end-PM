# analyze/models.py

from __future__ import annotations
# أعلى الملف:
import uuid
from django.db import models

STATUS_CHOICES = (
    ("pending", "Pending"),      # اتخزنت صور بس لسه مفيش دفع/تحليل
    ("paid", "Paid"),            # الدفع تمّ، ومحتاجين نعمل inference
    ("processed", "Processed"),  # اتعمل inference وتخزّن result
)

class AnalysisResult(models.Model):
    # ...
    analysis_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="pending")
    # باقي الحقول اللي عندك (user, session_id القديم لو موجود, result, rgb_image, thermal_image, created_at)

import os
import uuid
from django.conf import settings
from django.db import models
from django.utils.deconstruct import deconstructible

# اختياري: لو بتستخدمي نتايج ثابتة
CLASS_NAMES = ("Badly_damaged", "Dead", "Infected", "Non_infected")
RESULT_CHOICES = [(c, c) for c in CLASS_NAMES]


@deconstructible
class UploadToPath:
    """
    Callable آمن للـ migrations:
    analysis/<subdir>/<session_id>/<uuid>.<ext>
    """
    def __init__(self, subdir: str):
        self.subdir = subdir

    def __call__(self, instance: "AnalysisResult", filename: str) -> str:
        _, ext = os.path.splitext(filename)
        ext = (ext or "").lower()
        fname = f"{uuid.uuid4().hex}{ext}"
        sid = (instance.session_id or "no-session").strip().replace("/", "_")
        return f"analysis/{self.subdir}/{sid}/{fname}"


class AnalysisResult(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="analysis_results",
        help_text="User who triggered the analysis (optional).",
        verbose_name="User",
    )

    session_id = models.CharField("Session ID", max_length=128, db_index=True)
    result = models.CharField("Result", max_length=64, choices=RESULT_CHOICES)

    rgb_image = models.ImageField(
        "RGB image",
        upload_to=UploadToPath("rgb"),
        null=True,
        blank=True,
        help_text="First RGB image associated with this session.",
    )
    thermal_image = models.ImageField(
        "Thermal image",
        upload_to=UploadToPath("thermal"),
        null=True,
        blank=True,
        help_text="First Thermal image associated with this session.",
    )

    created_at = models.DateTimeField("Created at", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["session_id"]),
            models.Index(fields=["session_id", "-created_at"]),
        ]
        verbose_name = "Analysis result"
        verbose_name_plural = "Analysis results"

    def __str__(self) -> str:
        return f"{self.session_id} → {self.result}"


# ===== احذف ملفات الصور عند حذف/تغيير السجل (اختياري لكن مفيد) =====
from django.db.models.signals import post_delete, pre_save  # noqa: E402
from django.dispatch import receiver  # noqa: E402


@receiver(post_delete, sender=AnalysisResult)
def delete_files_on_row_delete(sender, instance, **kwargs):
    for f in (instance.rgb_image, instance.thermal_image):
        try:
            if f and f.name and f.storage.exists(f.name):
                f.storage.delete(f.name)
        except Exception:
            pass


@receiver(pre_save, sender=AnalysisResult)
def delete_old_files_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old = AnalysisResult.objects.get(pk=instance.pk)
    except AnalysisResult.DoesNotExist:
        return
    for field in ["rgb_image", "thermal_image"]:
        old_file = getattr(old, field)
        new_file = getattr(instance, field)
        if old_file and old_file.name != getattr(new_file, "name", None):
            try:
                if old_file.storage.exists(old_file.name):
                    old_file.storage.delete(old_file.name)
            except Exception:
                pass
