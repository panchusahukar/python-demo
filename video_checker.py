# video_checker.py

import cv2
import os
from image_detector import load_model, detect_image
import tempfile

def analyze_video(video_path):
    if not os.path.exists(video_path):
        return {"error": "Video file not found."}

    model = load_model("models/image_model.pth")

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return {"error": "Unable to open video file."}

    frame_count = 0
    fake_count = 0
    total_frames = 0
    temp_dir = tempfile.mkdtemp()

    while True:
        ret, frame = cap.read()
        if not ret or frame_count > 30:  # Check up to 30 frames
            break

        total_frames += 1
        frame_path = os.path.join(temp_dir, f"frame{frame_count}.jpg")
        cv2.imwrite(frame_path, frame)

        result = detect_image(frame_path, model)
        if result["label"] == "Fake":
            fake_count += 1

        frame_count += 1

    cap.release()

    fake_ratio = fake_count / total_frames
    label = "Fake" if fake_ratio > 0.3 else "Real"

    return {
        "label": label,
        "confidence": round(fake_ratio, 4),
        "frames_analyzed": total_frames
    }

# Example usage
if __name__ == "__main__":
    result = analyze_video("test_videos/sample.mp4")
    print(result)
