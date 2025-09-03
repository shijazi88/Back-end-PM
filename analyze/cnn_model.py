import torch
import torch.nn as nn
from torchvision import models   # Torch models

class DualInputCNN(nn.Module):
    def __init__(self, num_classes=4):
        super(DualInputCNN, self).__init__()
        self.rgb_model = models.resnet18(pretrained=True)
        self.rgb_model.fc = nn.Identity()

        self.thermal_model = models.resnet18(pretrained=True)
        self.thermal_model.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.thermal_model.fc = nn.Identity()

        self.classifier = nn.Sequential(
            nn.Linear(512 + 512, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, num_classes)
        )

    def forward(self, rgb_input, thermal_input):
        rgb_feat = self.rgb_model(rgb_input)
        thermal_feat = self.thermal_model(thermal_input)
        fused = torch.cat((rgb_feat, thermal_feat), dim=1)
        out = self.classifier(fused)
        return out
