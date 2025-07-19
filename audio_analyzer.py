# audio_analyzer.py

import librosa
import numpy as np
import os

def extract_features(audio_path):
    try:
        y, sr = librosa.load(audio_path, sr=16000)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mean_mfcc = np.mean(mfcc, axis=1)
        return mean_mfcc
    except Exception as e:
        return None

def detect_audio_fake(audio_path):
    if not os.path.exists(audio_path):
        return {"error": "Audio file not found."}

    features = extract_features(audio_path)
    if features is None:
        return {"error": "Failed to process audio."}

    # Simulate detection with dummy logic
    confidence = np.random.uniform(0.7, 0.99)
    label = "Fake" if features[0] < -50 else "Real"

    return {
        "label": label,
        "confidence": round(confidence, 4)
    }

# Example usage
if __name__ == "__main__":
    result = detect_audio_fake("test_audio/sample.wav")
    print(result)
