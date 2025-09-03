# analyze/views.py
import os
import torch
from PIL import Image
import torchvision.transforms as T
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .cnn_model import DualInputCNN
from .models import AnalysisResult

# ====== Model & transforms ======
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
IMAGE_SIZE = (224, 224)
CLASS_NAMES = ["Badly_damaged", "Dead", "Infected", "Non_infected"]

rgb_transform = T.Compose([T.Resize(IMAGE_SIZE), T.ToTensor()])
thermal_transform = T.Compose([T.Resize(IMAGE_SIZE), T.ToTensor()])

model_path = os.path.join(settings.BASE_DIR, "model_files", "palm_dualinput_model.pth")
model = DualInputCNN(num_classes=4)
model.load_state_dict(torch.load(model_path, map_location=DEVICE))
model.to(DEVICE)
model.eval()


class AnalyzeAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        try:
            rgb_files = request.FILES.getlist("rgb_images")
            thermal_files = request.FILES.getlist("thermal_images")
            session_id = request.data.get("session_id")

            if not session_id:
                return Response({"error": "session_id is required"}, status=status.HTTP_400_BAD_REQUEST)
            if not rgb_files or not thermal_files:
                return Response({"error": "Both rgb_images and thermal_images are required"}, status=status.HTTP_400_BAD_REQUEST)

            # اقرأ الصور وحوّلها لتنسورات
            rgb_imgs, thermal_imgs = [], []
            for f in rgb_files:
                img = Image.open(f).convert("RGB")
                rgb_imgs.append(rgb_transform(img))

            for f in thermal_files:
                img = Image.open(f).convert("L")
                thermal_imgs.append(thermal_transform(img))

            outputs = []
            with torch.no_grad():
                for rgb_img in rgb_imgs:
                    for thermal_img in thermal_imgs:
                        rgb_tensor = rgb_img.unsqueeze(0).to(DEVICE)
                        thermal_tensor = thermal_img.unsqueeze(0).to(DEVICE)
                        out = model(rgb_tensor, thermal_tensor)
                        outputs.append(out.cpu())

            if not outputs:
                return Response({"error": "No outputs generated from model"}, status=500)

            avg_output = torch.mean(torch.cat(outputs, dim=0), dim=0)
            pred_idx = torch.argmax(avg_output).item()
            pred_class = CLASS_NAMES[pred_idx]

            # خزّن أول صورة من كل نوع (أعد ضبط مؤشر الملف قبل الحفظ)
            rgb_file = rgb_files[0]
            thermal_file = thermal_files[0]
            try:
                rgb_file.seek(0)
            except Exception:
                pass
            try:
                thermal_file.seek(0)
            except Exception:
                pass

            analysis = AnalysisResult.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_id=session_id,
                result=pred_class,
                rgb_image=rgb_file,
                thermal_image=thermal_file,
            )

            return Response(
                {
                    "id": analysis.id,
                    "session_id": session_id,
                    "result": pred_class,
                    "rgb_image": request.build_absolute_uri(analysis.rgb_image.url) if analysis.rgb_image else None,
                    "thermal_image": request.build_absolute_uri(analysis.thermal_image.url) if analysis.thermal_image else None,
                },
                status=200,
            )

        except Exception as e:
            import traceback
            print("ERROR in AnalyzeAPIView:", traceback.format_exc())
            return Response({"error": str(e)}, status=500)


@api_view(["GET"])
@permission_classes([AllowAny])
def prediction_result(request):
    try:
        session_id = request.GET.get("session_id")
        if not session_id:
            return Response({"error": "session_id is required"}, status=400)

        analysis = AnalysisResult.objects.filter(session_id=session_id).last()
        if not analysis:
            return Response({"error": f"No result found for session_id={session_id}"}, status=404)

        return Response(
            {
                "session_id": session_id,
                "result": analysis.result,
                "rgb_image": request.build_absolute_uri(analysis.rgb_image.url) if analysis.rgb_image else None,
                "thermal_image": request.build_absolute_uri(analysis.thermal_image.url) if analysis.thermal_image else None,
            },
            status=200,
        )

    except Exception as e:
        import traceback
        print("ERROR in prediction_result:", traceback.format_exc())
        return Response({"error": str(e)}, status=500)


@api_view(["GET"])
@permission_classes([AllowAny])
def ping(request):
    # راوت بسيط للتأكد إن include شغال
    return Response({"ok": True, "where": "analyze.urls"}, status=200)
