# image_detector.py

import torch
import torchvision.transforms as transforms
from PIL import Image
import os

# Load your trained model (replace with your actual path and class)
class SimpleCNN(torch.nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = torch.nn.Conv2d(3, 16, kernel_size=3)
        self.pool = torch.nn.MaxPool2d(2, 2)
        self.fc1 = torch.nn.Linear(16 * 62 * 62, 2)  # Adjust depending on image size

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = x.view(-1, 16 * 62 * 62)
        x = self.fc1(x)
        return x

# Load the model
def load_model(model_path="models/image_model.pth"):
    model = SimpleCNN()
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()
    return model

# Preprocessing for image
transform = transforms.Compose([
    transforms.Resize((128, 128)),     # Resize image
    transforms.ToTensor(),             # Convert to tensor
    transforms.Normalize([0.5]*3, [0.5]*3)  # Normalize
])

def detect_image(image_path, model):
    """
    Detects whether an image is real or fake using the trained model.
    """
    if not os.path.exists(image_path):
        return {"error": "Image file not found."}

    image = Image.open(image_path).convert("RGB")
    img_tensor = transform(image).unsqueeze(0)  # Add batch dimension

    with torch.no_grad():
        output = model(img_tensor)
        _, predicted = torch.max(output.data, 1)
        label = "Fake" if predicted.item() == 1 else "Real"
        confidence = torch.nn.functional.softmax(output, dim=1)[0][predicted.item()].item()

    return {
        "label": label,
        "confidence": round(confidence, 4)
    }

# Test the module
if __name__ == "__main__":
    model = load_model("models/image_model.pth")
    result = detect_image("test_images/sample.jpg", model)
    print(result)
