from django.db.models.signals import post_delete
from django.dispatch import receiver

@receiver(post_delete, sender=AnalysisResult)
def _delete_files_on_row_delete(sender, instance: AnalysisResult, **kwargs):
    for f in (instance.rgb_image, instance.thermal_image):
        try:
            if f and f.name and f.storage.exists(f.name):
                f.storage.delete(f.name)
        except Exception:
            # ما نوقعش الحذف لو التخزين مش لاقي الملف
            pass
