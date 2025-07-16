# text_classifier.py

from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline
import torch

# Load pre-trained tokenizer and model (you can use a fine-tuned fake news model)
MODEL_NAME = "mrm8488/bert-tiny-finetuned-fake-news"

# Load tokenizer and model
tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
model = BertForSequenceClassification.from_pretrained(MODEL_NAME)

# Create pipeline for inference
classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

def classify_text(text):
    """
    Classifies the input text as real or fake.
    """
    result = classifier(text)[0]
    label = result['label']
    score = result['score']

    # Map label to custom output
    if label.lower() == 'real':
        prediction = 'Real News'
    elif label.lower() == 'fake':
        prediction = 'Fake News'
    else:
        prediction = label

    return {
        'label': prediction,
        'score': round(score, 4)
    }

# Example usage
if __name__ == "__main__":
    sample_text = input("Enter text to verify: ")
    result = classify_text(sample_text)
    print(f"Prediction: {result['label']} (Confidence: {result['score']})")
