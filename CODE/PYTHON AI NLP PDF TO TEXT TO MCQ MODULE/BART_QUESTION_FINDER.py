from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Step 1: Load Pre-trained Model and Tokenizer
model_name = "bert-base-uncased"  # BERT pre-trained model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)  # 2 labels: MCQ and Numerical

# Step 2: Define Sample Data
texts = [
    "What is the capital of France? A. Paris B. Berlin C. Madrid D. Rome",
    "Calculate the square root of 64."
]
labels = ["MCQ", "Numerical"]  # For testing purposes

# Step 3: Tokenize Input
inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")

# Step 4: Predict Using the Model
outputs = model(**inputs)
logits = outputs.logits
predictions = torch.argmax(logits, dim=1)

# Map Predictions Back to Labels
label_map = {0: "MCQ", 1: "Numerical"}
predicted_labels = [label_map[p.item()] for p in predictions]

# Print Results
for text, label in zip(texts, predicted_labels):
    print(f"Text: {text}\nPredicted Label: {label}\n")
