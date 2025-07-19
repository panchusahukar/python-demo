# inference_api.py

from flask import Flask, request, jsonify
from text_classifier import classify_text
from image_detector import load_model, detect_image
from video_checker import analyze_video
from audio_analyzer import detect_audio_fake
import os

app = Flask(__name__)
image_model = load_model("models/image_model.pth")

@app.route("/detect/text", methods=["POST"])
def detect_text():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Text is required"}), 400

    result = classify_text(data["text"])
    return jsonify(result)

@app.route("/detect/image", methods=["POST"])
def detect_image_api():
    if "image" not in request.files:
        return jsonify({"error": "Image file is required"}), 400

    file = request.files["image"]
    path = os.path.join("uploads", file.filename)
    file.save(path)

    result = detect_image(path, image_model)
    os.remove(path)
    return jsonify(result)

@app.route("/detect/video", methods=["POST"])
def detect_video_api():
    if "video" not in request.files:
        return jsonify({"error": "Video file is required"}), 400

    file = request.files["video"]
    path = os.path.join("uploads", file.filename)
    file.save(path)

    result = analyze_video(path)
    os.remove(path)
    return jsonify(result)

@app.route("/detect/audio", methods=["POST"])
def detect_audio_api():
    if "audio" not in request.files:
        return jsonify({"error": "Audio file is required"}), 400

    file = request.files["audio"]
    path = os.path.join("uploads", file.filename)
    file.save(path)

    result = detect_audio_fake(path)
    os.remove(path)
    return jsonify(result)

if __name__ == "__main__":
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    app.run(debug=True)
